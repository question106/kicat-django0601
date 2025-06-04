from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime, timedelta
import os


class QuotePDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.buffer = BytesIO()
        
        # KICAT Brand Colors
        self.primary_color = colors.HexColor('#710600')  # KICAT Primary Red
        self.secondary_color = colors.HexColor('#d09101')  # KICAT Secondary Gold
        self.accent_color = colors.HexColor('#f8f9fa')  # Light background
        self.text_color = colors.HexColor('#2c3e50')  # Dark text
        self.muted_color = colors.HexColor('#6c757d')  # Muted text
        
        # Register Noto Sans Korean fonts
        try:
            # Get the path to the static fonts directory
            font_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'fonts', 'Noto_Sans_KR', 'static')
            
            # Register different weights of Noto Sans KR
            noto_regular_path = os.path.join(font_dir, 'NotoSansKR-Regular.ttf')
            noto_bold_path = os.path.join(font_dir, 'NotoSansKR-Bold.ttf')
            noto_medium_path = os.path.join(font_dir, 'NotoSansKR-Medium.ttf')
            noto_light_path = os.path.join(font_dir, 'NotoSansKR-Light.ttf')
            
            # Register the fonts
            if os.path.exists(noto_regular_path):
                pdfmetrics.registerFont(TTFont('NotoSansKR-Regular', noto_regular_path))
                self.font = 'NotoSansKR-Regular'
                print("✅ Registered NotoSansKR-Regular font")
            else:
                raise FileNotFoundError("NotoSansKR-Regular.ttf not found")
                
            if os.path.exists(noto_bold_path):
                pdfmetrics.registerFont(TTFont('NotoSansKR-Bold', noto_bold_path))
                self.font_bold = 'NotoSansKR-Bold'
                print("✅ Registered NotoSansKR-Bold font")
            else:
                self.font_bold = self.font
                
            if os.path.exists(noto_medium_path):
                pdfmetrics.registerFont(TTFont('NotoSansKR-Medium', noto_medium_path))
                self.font_medium = 'NotoSansKR-Medium'
                print("✅ Registered NotoSansKR-Medium font")
            else:
                self.font_medium = self.font
                
            if os.path.exists(noto_light_path):
                pdfmetrics.registerFont(TTFont('NotoSansKR-Light', noto_light_path))
                self.font_light = 'NotoSansKR-Light'
                print("✅ Registered NotoSansKR-Light font")
            else:
                self.font_light = self.font
                
            print(f"✅ Successfully registered Noto Sans KR fonts for Korean language support")
            
        except Exception as e:
            print(f"⚠️ Failed to register Noto Sans KR fonts: {e}")
            # Fallback directly to Arial since HeiseiMin-W3 doesn't support Korean
            self.font = 'Arial'
            self.font_bold = 'Arial-Bold'
            self.font_medium = 'Arial'
            self.font_light = 'Arial'
            print("⚠️ Using Arial fallback font (Noto Sans KR not available)")
        
        print(f"Using primary font: {self.font}")
        
    def generate_quote_pdf(self, quote):
        """Generate a professional PDF quote for the given Quote object"""
        doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=1.5*cm,
            bottomMargin=2*cm
        )
        
        # Build PDF content
        story = []
        
        # Header with company branding
        story.extend(self._create_header(quote))
        story.append(Spacer(1, 0.8*cm))
        
        # Quote information banner
        story.extend(self._create_quote_info_banner(quote))
        story.append(Spacer(1, 0.6*cm))
        
        # Client information card
        story.extend(self._create_client_info_card(quote))
        story.append(Spacer(1, 0.6*cm))
        
        # Service details section
        story.extend(self._create_service_details(quote))
        story.append(Spacer(1, 0.8*cm))
        
        # Terms and conditions
        story.extend(self._create_terms_section())
        story.append(Spacer(1, 1*cm))
        
        # Footer with signature
        story.extend(self._create_footer_section())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_content
    
    def _create_header(self, quote):
        """Create modern header with company branding and Korean support"""
        elements = []
        
        # Top border line
        top_line = Table([['']]) 
        top_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 3, self.primary_color),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(top_line)
        elements.append(Spacer(1, 0.3*cm))
        
        # Company header with Korean and English names
        company_name_kr = "한국통번역주식회사"
        company_name_en = "Korea Translation & Interpretation Co., Ltd."
        tagline = "Professional Translation & Interpretation Services"
        
        # Header content with Korean company name
        header_left = f"""
        <font size="18" color="#710600" name="{self.font_bold}"><b>{company_name_kr}</b></font><br/>
        <font size="14" color="#710600" name="{self.font_medium}"><b>{company_name_en}</b></font><br/>
        <font size="11" color="#6c757d" name="{self.font}">{tagline}</font>
        """
        
        # Contact info aligned right with Korean labels
        contact_info = f"""
        <font size="9" color="#2c3e50" name="{self.font}">
        <b>서울시 강남구 테헤란로, 116, 10층 1055호</b><br/>
        <b>Seoul, Gangnam-gu, South Korea</b><br/>
        전화 (Phone): +82-2-6265-6159<br/>
        이메일 (Email): kicat@kicat.co.kr
        </font>
        """
        
        # Create Korean-compatible styles
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=11,
            leading=14
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=9,
            leading=11
        )
        
        header_data = [[Paragraph(header_left, header_style), 
                       Paragraph(contact_info, contact_style)]]
        
        header_table = Table(header_data, colWidths=[11*cm, 7*cm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.4*cm))
        
        return elements
    
    def _create_quote_info_banner(self, quote):
        """Create quote information banner"""
        elements = []
        
        current_date = datetime.now()
        
        # Quote banner with gradient-like effect
        quote_number = f"견적서 #{quote.id:04d}"
        quote_date = current_date.strftime('%Y/%m/%d')
        valid_until = (current_date + timedelta(days=14)).strftime('%Y/%m/%d')
        
        banner_content = f"""
        <font size="24" color="white" name="{self.font_bold}"><b>{quote_number}</b></font>
        """
        
        date_content = f"""
        <font size="10" color="white" name="{self.font}">
        <b>발행일:</b> {quote_date}<br/>
        <b>유효기간:</b> {valid_until}<br/>
        <b>고객번호:</b> {quote.id:06d}
        </font>
        """
        
        # Create Korean-compatible styles for banner
        banner_style = ParagraphStyle(
            'BannerStyle',
            parent=self.styles['Normal'],
            fontName=self.font_bold,
            fontSize=24,
            leading=28
        )
        
        date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=10,
            leading=13
        )
        
        banner_data = [[Paragraph(banner_content, banner_style), 
                       Paragraph(date_content, date_style)]]
        
        banner_table = Table(banner_data, colWidths=[10*cm, 8*cm])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.primary_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(banner_table)
        
        return elements
    
    def _create_client_info_card(self, quote):
        """Create client information card with modern styling"""
        elements = []
        
        # Section title with medium weight font
        title_style = ParagraphStyle(
            'ClientTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font_medium,
            textColor=self.primary_color,
            spaceAfter=10,
            spaceBefore=5
        )
        
        elements.append(Paragraph("고객 정보 (CLIENT INFORMATION)", title_style))
        
        # Client details in a card-like format with Korean support
        client_info = f"""
        <font size="11" color="#2c3e50" name="{self.font}">
        <b>회사명 (Company):</b> {quote.company or '미기재'}<br/>
        <b>담당자 (Contact Person):</b> {quote.name or '미기재'}<br/>
        <b>전화번호 (Phone):</b> {quote.phone or '미기재'}<br/>
        <b>이메일 (Email):</b> {quote.email or '미기재'}
        </font>
        """
        
        # Service request details with Korean support
        service_info = f"""
        <font size="11" color="#2c3e50" name="{self.font}">
        <b>서비스 유형 (Service Type):</b> {quote.service_type.name}<br/>
        <b>카테고리 (Category):</b> {quote.service_type.category.name}<br/>
        <b>요청일 (Request Date):</b> {quote.created_at.strftime('%Y/%m/%d')}
        </font>
        """
        
        # Create custom style for Korean text
        korean_style = ParagraphStyle(
            'KoreanStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=11,
            leading=14
        )
        
        info_data = [[Paragraph(client_info, korean_style), 
                     Paragraph(service_info, korean_style)]]
        
        info_table = Table(info_data, colWidths=[9*cm, 9*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.accent_color),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#e9ecef')),
        ]))
        
        elements.append(info_table)
        
        # Add project description if available with Korean support
        if quote.message:
            elements.append(Spacer(1, 0.3*cm))
            desc_title = Paragraph("프로젝트 설명 (PROJECT DESCRIPTION)", title_style)
            elements.append(desc_title)
            
            desc_content = f"""
            <font size="10" color="#2c3e50" name="{self.font}">
            {quote.message}
            </font>
            """
            
            desc_table = Table([[Paragraph(desc_content, korean_style)]], colWidths=[18*cm])
            desc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#ffeaa7')),
            ]))
            elements.append(desc_table)
        
        return elements
    
    def _create_service_details(self, quote):
        """Create enhanced service details table"""
        elements = []
        
        # Section title with medium weight font and Korean support
        title_style = ParagraphStyle(
            'ServiceTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font_medium,
            textColor=self.primary_color,
            spaceAfter=15,
            spaceBefore=5
        )
        
        elements.append(Paragraph("서비스 상세 및 견적 (SERVICE DETAILS & PRICING)", title_style))
        
        # Service table with enhanced styling and Korean headers
        header_data = [["설명 (Description)", "수량 (Qty)", "단가 (Unit Price)", "합계 (Total)"]]
        
        # Get quote items or create default if none exist
        quote_items = quote.items.all()
        service_data = []
        
        # Create a Korean-compatible style for table cells
        korean_cell_style = ParagraphStyle(
            'KoreanCellStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=11,
            leading=14
        )
        
        if quote_items.exists():
            # Use actual quote items
            for item in quote_items:
                # Wrap Korean text in Paragraph with proper font
                description = Paragraph(f'<font name="{self.font}">{item.item_description}</font>', korean_cell_style)
                quantity = Paragraph(f'<font name="{self.font}">{str(item.quantity)}</font>', korean_cell_style)
                unit_price = Paragraph(f'<font name="{self.font}">₩{item.unit_price:,.2f}</font>', korean_cell_style)
                total_price = Paragraph(f'<font name="{self.font}">₩{item.total_price:,.2f}</font>', korean_cell_style)
                
                service_data.append([description, quantity, unit_price, total_price])
        else:
            # Fallback to default service if no items exist
            service_description = f"{quote.service_type.name}"
            if quote.message and len(quote.message) > 30:
                service_description += f"\n{quote.message[:50]}..."
            
            # Wrap Korean text in Paragraph with proper font
            description = Paragraph(f'<font name="{self.font}">{service_description}</font>', korean_cell_style)
            quantity = Paragraph(f'<font name="{self.font}">1</font>', korean_cell_style)
            unit_price = Paragraph(f'<font name="{self.font}">₩500,000.00</font>', korean_cell_style)
            total_price = Paragraph(f'<font name="{self.font}">₩500,000.00</font>', korean_cell_style)
            
            service_data.append([description, quantity, unit_price, total_price])
        
        table_data = header_data + service_data
        
        service_table = Table(table_data, colWidths=[8.5*cm, 2.5*cm, 3.5*cm, 3.5*cm])
        service_table.setStyle(TableStyle([
            # Header styling with Korean font
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.font_medium),
            ('FONTNAME', (0, 1), (-1, -1), self.font),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Row styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.text_color),
            
            # Borders
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.white),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('LINEBEFORE', (0, 0), (0, -1), 1, self.primary_color),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, self.primary_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(service_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # Enhanced summary section using quote model calculations with Korean labels
        if quote_items.exists():
            subtotal = quote.subtotal
            tax_amount = quote.tax_amount
            total_amount = quote.total_amount
        else:
            # Fallback values
            from decimal import Decimal
            subtotal = Decimal('500000.00')
            tax_amount = subtotal * Decimal('0.00')  # No tax
            total_amount = subtotal + tax_amount
        
        summary_data = [
            ["", "", "소계 (Subtotal):", f"₩{subtotal:,.2f}"],
            ["", "", "세금 (Tax):", f"₩{tax_amount:,.2f}"],
            ["", "", "", ""],  # Spacer row
            ["", "", "총 금액 (TOTAL AMOUNT):", f"₩{total_amount:,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[6*cm, 3*cm, 5*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), self.font),
            ('FONTNAME', (0, -1), (-1, -1), self.font_bold),
            ('FONTSIZE', (0, 0), (-1, -2), 11),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, 0), (-1, -2), self.text_color),
            
            # Total row highlighting - only for label and value cells
            ('BACKGROUND', (2, -1), (-1, -1), self.secondary_color),
            ('TEXTCOLOR', (2, -1), (-1, -1), colors.white),
            
            # Borders
            ('LINEABOVE', (2, -1), (-1, -1), 2, self.secondary_color),
            ('LINEBELOW', (2, -1), (-1, -1), 2, self.secondary_color),
            ('LINEBEFORE', (2, 0), (2, -1), 1, colors.HexColor('#dee2e6')),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('INNERGRID', (2, 0), (-1, -2), 0.5, colors.HexColor('#dee2e6')),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -2), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -2), 6),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        
        return elements
    
    def _create_terms_section(self):
        """Create enhanced terms and conditions section with Korean support"""
        elements = []
        
        # Section title with Korean and English
        title_style = ParagraphStyle(
            'TermsTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font_medium,
            textColor=self.primary_color,
            spaceAfter=10,
            spaceBefore=5
        )
        
        elements.append(Paragraph("이용약관 (TERMS & CONDITIONS)", title_style))
        
        # Terms content with Korean and English and proper font
        terms_content = f"""
        <font size="10" color="#2c3e50" name="{self.font}">
        <b>1. 견적 유효기간 (Quote Validity):</b> 본 견적서는 발행일로부터 30일간 유효합니다.<br/><br/>
        <b>2. 결제 조건 (Payment Terms):</b> 서비스 시작 전에 결제가 완료되어야 합니다.<br/><br/>
        <b>3. 서비스 제공 (Service Delivery):</b> 예상 완료 시간은 프로젝트 승인 시 확정됩니다.<br/><br/>
        <b>4. 변경 사항 (Modifications):</b> 추가 요구사항이나 변경 시 견적이 수정될 수 있습니다.<br/><br/>
        <b>5. 품질 보증 (Quality Assurance):</b> 모든 서비스에는 품질 검토 및 고객 승인 과정이 포함됩니다.
        </font>
        """
        
        # Create Korean-compatible style
        korean_terms_style = ParagraphStyle(
            'KoreanTermsStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=10,
            leading=13
        )
        
        terms_table = Table([[Paragraph(terms_content, korean_terms_style)]], colWidths=[18*cm])
        terms_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LINEBEFORE', (0, 0), (0, -1), 3, self.secondary_color),
        ]))
        
        elements.append(terms_table)
        
        return elements
    
    def _create_footer_section(self):
        """Create professional footer with signature area and Korean support"""
        elements = []
        
        # Thank you message with Korean and English
        thank_you_style = ParagraphStyle(
            'ThankYou',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName=self.font,
            textColor=self.primary_color,
            alignment=TA_CENTER,
            spaceAfter=15
        )
        
        elements.append(Paragraph("한국통번역주식회사를 선택해 주셔서 감사합니다.", thank_you_style))
        elements.append(Paragraph("Thank you for choosing Korea Translation & Interpretation Co., Ltd.", thank_you_style))
        
        # Signature section with Korean and English labels
        signature_content = f"""
        <font size="11" color="#2c3e50" name="{self.font}">
        <b>견적을 진행하시려면 아래에 서명하여 회신해 주시기 바랍니다.</b><br/>
        <b>To proceed with this quote, please sign below and return to us:</b>
        </font>
        """
        
        korean_signature_style = ParagraphStyle(
            'KoreanSignatureStyle',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=11,
            leading=14
        )
        
        elements.append(Paragraph(signature_content, korean_signature_style))
        elements.append(Spacer(1, 0.4*cm))
        
        # Signature fields with Korean labels
        signature_data = [
            ["고객 서명 (Client Signature)", "날짜 (Date)", "KICAT 담당자 (Representative)"],
            ["", "", ""],
            ["_" * 25, "_" * 15, "_" * 25],
            ["", "", ""],
            [f"성명 (Print Name): ____________", f"날짜 (Date): ______", "한국통번역주식회사 승인"]
        ]
        
        signature_table = Table(signature_data, colWidths=[6*cm, 4*cm, 8*cm])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 2), (-1, 2), 8),
            ('FONTSIZE', (0, 4), (-1, 4), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.text_color),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 2), (-1, 2), 5),
        ]))
        
        elements.append(signature_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Footer line
        footer_line = Table([['']]) 
        footer_line.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 2, self.primary_color),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(footer_line)
        
        return elements


def generate_quote_pdf(quote):
    """Utility function to generate PDF for a quote"""
    generator = QuotePDFGenerator()
    pdf_content = generator.generate_quote_pdf(quote)
    
    # Create filename
    filename = f"KICAT_Quote_{quote.id:04d}_{quote.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Create ContentFile
    pdf_file = ContentFile(pdf_content, filename)
    
    return pdf_file 