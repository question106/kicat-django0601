import os
import re
import json
import html
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from pathlib import Path


class Command(BaseCommand):
    help = 'Extract all text from templates and models for translation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'txt', 'csv'],
            default='json',
            help='Output format (default: json)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='extracted_texts',
            help='Output filename (without extension)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting text extraction...'))
        
        extracted_data = {
            'templates': {},
            'models': {},
            'summary': {}
        }
        
        # Extract from templates
        template_texts = self.extract_from_templates()
        extracted_data['templates'] = template_texts
        
        # Extract from models
        model_texts = self.extract_from_models()
        extracted_data['models'] = model_texts
        
        # Generate summary
        total_template_texts = sum(len(texts) for texts in template_texts.values())
        total_model_texts = sum(len(texts) for texts in model_texts.values())
        
        extracted_data['summary'] = {
            'total_templates': len(template_texts),
            'total_template_texts': total_template_texts,
            'total_models': len(model_texts),
            'total_model_texts': total_model_texts,
            'total_texts': total_template_texts + total_model_texts
        }
        
        # Save to file
        self.save_extracted_data(extracted_data, options['format'], options['output'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully extracted {extracted_data["summary"]["total_texts"]} text entries!'
            )
        )

    def extract_from_templates(self):
        """Extract text from all HTML templates"""
        self.stdout.write('Extracting from templates...')
        
        template_texts = {}
        template_dirs = self.get_template_directories()
        
        for template_dir in template_dirs:
            for template_file in Path(template_dir).rglob('*.html'):
                if self.should_skip_template(template_file):
                    continue
                    
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse template and extract texts
                    texts = self.parse_template_content(content)
                    if texts:
                        relative_path = str(template_file.relative_to(Path(settings.BASE_DIR)))
                        template_texts[relative_path] = texts
                        
                        self.stdout.write(f'  ✓ {relative_path}: {len(texts)} texts')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ✗ Error reading {template_file}: {e}')
                    )
        
        return template_texts

    def extract_from_models(self):
        """Extract text from model fields and choices"""
        self.stdout.write('Extracting from models...')
        
        model_texts = {}
        
        # Get all models from our apps (excluding admin, auth, etc.)
        our_apps = ['core', 'quotes']  # Add your app names here
        
        for app_name in our_apps:
            try:
                app_models = apps.get_app_config(app_name).get_models()
                
                for model in app_models:
                    model_name = f"{app_name}.{model.__name__}"
                    texts = self.extract_model_texts(model)
                    
                    if texts:
                        model_texts[model_name] = texts
                        self.stdout.write(f'  ✓ {model_name}: {len(texts)} texts')
                        
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'  ✗ Error processing app {app_name}: {e}')
                )
        
        return model_texts

    def get_template_directories(self):
        """Get all template directories"""
        template_dirs = []
        
        # From TEMPLATES setting
        for template_config in settings.TEMPLATES:
            if 'DIRS' in template_config:
                template_dirs.extend(template_config['DIRS'])
        
        # From app directories
        for app_config in apps.get_app_configs():
            app_template_dir = Path(app_config.path) / 'templates'
            if app_template_dir.exists():
                template_dirs.append(str(app_template_dir))
        
        return template_dirs

    def should_skip_template(self, template_file):
        """Check if template should be skipped"""
        skip_patterns = [
            'admin',
            'registration',
            'debug',
            'test'
        ]
        
        file_str = str(template_file).lower()
        return any(pattern in file_str for pattern in skip_patterns)

    def parse_template_content(self, content):
        """Parse template content and extract text using regex"""
        texts = []
        
        # Remove Django template tags and comments but keep the content
        content = re.sub(r'{%.*?%}', '', content, flags=re.DOTALL)
        content = re.sub(r'{#.*?#}', '', content, flags=re.DOTALL)
        
        # Remove script and style content
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract text from HTML tags using regex
        # This is a simple approach - gets text between tags
        text_pattern = r'>([^<]+)<'
        matches = re.findall(text_pattern, content)
        
        for match in matches:
            text = html.unescape(match.strip())
            if text and self.is_translatable_text(text):
                # Clean up Django template variables
                clean_text = re.sub(r'{{.*?}}', '[VARIABLE]', text)
                if clean_text.strip():
                    texts.append({
                        'original': text,
                        'clean': clean_text.strip(),
                        'context': 'html_content'
                    })
        
        # Extract from common attributes
        attr_patterns = [
            r'title\s*=\s*["\']([^"\']+)["\']',
            r'alt\s*=\s*["\']([^"\']+)["\']',
            r'placeholder\s*=\s*["\']([^"\']+)["\']',
            r'value\s*=\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in attr_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                attr_text = html.unescape(match.strip())
                if attr_text and self.is_translatable_text(attr_text):
                    texts.append({
                        'original': attr_text,
                        'clean': attr_text,
                        'context': 'html_attribute'
                    })
        
        return texts

    def extract_model_texts(self, model):
        """Extract translatable texts from model"""
        texts = []
        
        # Model meta information
        if hasattr(model._meta, 'verbose_name') and model._meta.verbose_name:
            texts.append({
                'type': 'model_verbose_name',
                'original': str(model._meta.verbose_name),
                'context': f'{model.__name__} verbose_name'
            })
        
        if hasattr(model._meta, 'verbose_name_plural') and model._meta.verbose_name_plural:
            texts.append({
                'type': 'model_verbose_name_plural',
                'original': str(model._meta.verbose_name_plural),
                'context': f'{model.__name__} verbose_name_plural'
            })
        
        # Field information
        for field in model._meta.get_fields():
            # Field verbose names
            if hasattr(field, 'verbose_name') and field.verbose_name:
                texts.append({
                    'type': 'field_verbose_name',
                    'original': str(field.verbose_name),
                    'context': f'{model.__name__}.{field.name} verbose_name'
                })
            
            # Field help texts
            if hasattr(field, 'help_text') and field.help_text:
                texts.append({
                    'type': 'field_help_text',
                    'original': str(field.help_text),
                    'context': f'{model.__name__}.{field.name} help_text'
                })
            
            # Choice field options
            if hasattr(field, 'choices') and field.choices:
                for choice_value, choice_label in field.choices:
                    if choice_label and self.is_translatable_text(str(choice_label)):
                        texts.append({
                            'type': 'field_choice',
                            'original': str(choice_label),
                            'context': f'{model.__name__}.{field.name} choice: {choice_value}'
                        })
        
        return texts

    def is_translatable_text(self, text):
        """Check if text should be translated"""
        if not text or len(text.strip()) < 2:
            return False
        
        # Skip common non-translatable patterns
        skip_patterns = [
            r'^\s*$',  # Empty or whitespace
            r'^[\d\s\-_\.]+$',  # Only numbers, spaces, dashes, underscores, dots
            r'^[A-Za-z0-9_\-\.]+\.(jpg|jpeg|png|gif|svg|css|js).*$',  # File names
            r'^https?://',  # URLs
            r'^[A-Za-z0-9_\-\.]+@[A-Za-z0-9_\-\.]+$',  # Email addresses
            r'^\w+$',  # Single words without spaces (likely IDs or technical terms)
            r'^[\s\n\r\t]+$',  # Only whitespace characters
        ]
        
        for pattern in skip_patterns:
            if re.match(pattern, text.strip(), re.IGNORECASE):
                return False
        
        # Check if text contains Korean characters (good indicator for your site)
        if re.search(r'[가-힣]', text):
            return True
        
        # Check if it's substantial English text (more than just a single word)
        if re.search(r'[A-Za-z].*\s+.*[A-Za-z]', text):
            return True
        
        return False

    def save_extracted_data(self, data, format_type, filename):
        """Save extracted data to file"""
        output_dir = Path(settings.BASE_DIR) / 'extracted_texts'
        output_dir.mkdir(exist_ok=True)
        
        if format_type == 'json':
            output_file = output_dir / f'{filename}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format_type == 'txt':
            output_file = output_dir / f'{filename}.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("TEMPLATE TEXTS\n")
                f.write("=" * 50 + "\n\n")
                
                for template, texts in data['templates'].items():
                    f.write(f"Template: {template}\n")
                    f.write("-" * 30 + "\n")
                    for text_info in texts:
                        f.write(f"• {text_info['clean']}\n")
                    f.write("\n")
                
                f.write("\nMODEL TEXTS\n")
                f.write("=" * 50 + "\n\n")
                
                for model, texts in data['models'].items():
                    f.write(f"Model: {model}\n")
                    f.write("-" * 30 + "\n")
                    for text_info in texts:
                        f.write(f"• {text_info['original']} ({text_info['type']})\n")
                    f.write("\n")
        
        elif format_type == 'csv':
            import csv
            output_file = output_dir / f'{filename}.csv'
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Source', 'Type', 'Original Text', 'Clean Text', 'Context'])
                
                for template, texts in data['templates'].items():
                    for text_info in texts:
                        writer.writerow([
                            template,
                            'template',
                            text_info['original'],
                            text_info['clean'],
                            text_info.get('context', '')
                        ])
                
                for model, texts in data['models'].items():
                    for text_info in texts:
                        writer.writerow([
                            model,
                            text_info['type'],
                            text_info['original'],
                            text_info['original'],
                            text_info['context']
                        ])
        
        self.stdout.write(
            self.style.SUCCESS(f'Text extraction saved to: {output_file}')
        ) 