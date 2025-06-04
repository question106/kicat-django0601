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
        
        # Register fonts with proper error handling
        try:
            # Try multiple fonts for better support
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
            self.font = 'HeiseiMin-W3'
            print("✅ Registered HeiseiMin-W3 font")
        except Exception as e:
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
                self.font = 'HeiseiKakuGo-W5'
                print("✅ Registered HeiseiKakuGo-W5 font")
            except Exception as e2:
                try:
                    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
                    self.font = 'STSong-Light'
                    print("✅ Registered STSong-Light font")
                except Exception as e3:
                    self.font = 'Helvetica'
                    print(f"⚠️ Using Helvetica fallback. Errors: {e}, {e2}, {e3}")
                
        print(f"Using font: {self.font}")
        
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
        """Create modern header with company branding"""
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
        
        # Company header with logo space and contact info
        company_name = "Korea Translation & Interpretation Co., Ltd."
        tagline = "Professional Translation & Interpretation Services"
        
        # Header content
        header_left = f"""
        <font size="20" color="#710600"><b>{company_name}</b></font><br/>
        <font size="11" color="#6c757d">{tagline}</font>
        """
        
        # Contact info aligned right
        contact_info = f"""
        <font size="9" color="#2c3e50">
        <b>Seoul, Gangnam-gu, South Korea</b><br/>
        Phone: +82-2-6265-6159<br/>
        Email: kicat@kicat.co.kr
        </font>
        """
        
        header_data = [[Paragraph(header_left, self.styles['Normal']), 
                       Paragraph(contact_info, self.styles['Normal'])]]
        
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
        quote_number = f"QUOTE #{quote.id:04d}"
        quote_date = current_date.strftime('%B %d, %Y')
        valid_until = (current_date + timedelta(days=30)).strftime('%B %d, %Y')
        
        banner_content = f"""
        <font size="24" color="white"><b>{quote_number}</b></font>
        """
        
        date_content = f"""
        <font size="10" color="white">
        <b>Issue Date:</b> {quote_date}<br/>
        <b>Valid Until:</b> {valid_until}<br/>
        <b>Client ID:</b> {quote.id:06d}
        </font>
        """
        
        banner_data = [[Paragraph(banner_content, self.styles['Normal']), 
                       Paragraph(date_content, self.styles['Normal'])]]
        
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
        
        # Section title
        title_style = ParagraphStyle(
            'ClientTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font,
            textColor=self.primary_color,
            spaceAfter=10,
            spaceBefore=5
        )
        
        elements.append(Paragraph("CLIENT INFORMATION", title_style))
        
        # Client details in a card-like format
        client_info = f"""
        <font size="11" color="#2c3e50">
        <b>Company:</b> {quote.company or 'Not specified'}<br/>
        <b>Contact Person:</b> {quote.name or 'Not specified'}<br/>
        <b>Phone:</b> {quote.phone or 'Not specified'}<br/>
        <b>Email:</b> {quote.email or 'Not specified'}
        </font>
        """
        
        # Service request details
        service_info = f"""
        <font size="11" color="#2c3e50">
        <b>Service Type:</b> {quote.service_type.name}<br/>
        <b>Category:</b> {quote.service_type.category.name}<br/>
        <b>Request Date:</b> {quote.created_at.strftime('%B %d, %Y')}
        </font>
        """
        
        info_data = [[Paragraph(client_info, self.styles['Normal']), 
                     Paragraph(service_info, self.styles['Normal'])]]
        
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
        
        # Add project description if available
        if quote.message:
            elements.append(Spacer(1, 0.3*cm))
            desc_title = Paragraph("PROJECT DESCRIPTION", title_style)
            elements.append(desc_title)
            
            desc_content = f"""
            <font size="10" color="#2c3e50">
            {quote.message}
            </font>
            """
            
            desc_table = Table([[Paragraph(desc_content, self.styles['Normal'])]], colWidths=[18*cm])
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
        
        # Section title
        title_style = ParagraphStyle(
            'ServiceTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font,
            textColor=self.primary_color,
            spaceAfter=15,
            spaceBefore=5
        )
        
        elements.append(Paragraph("SERVICE DETAILS & PRICING", title_style))
        
        # Service table with enhanced styling
        header_data = [["Description", "Qty", "Unit Price", "Total"]]
        
        # Get quote items or create default if none exist
        quote_items = quote.items.all()
        service_data = []
        
        if quote_items.exists():
            # Use actual quote items
            for item in quote_items:
                service_data.append([
                    item.item_description,
                    str(item.quantity),
                    f"₩{item.unit_price:,.2f}",
                    f"₩{item.total_price:,.2f}"
                ])
        else:
            # Fallback to default service if no items exist
            service_description = f"{quote.service_type.name}"
            if quote.message and len(quote.message) > 30:
                service_description += f"\n{quote.message[:50]}..."
            
            service_data.append([
                service_description,
                "1",
                "₩500,000.00",
                "₩500,000.00"
            ])
        
        table_data = header_data + service_data
        
        service_table = Table(table_data, colWidths=[8.5*cm, 2.5*cm, 3.5*cm, 3.5*cm])
        service_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), self.font),
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
        
        # Enhanced summary section using quote model calculations
        if quote_items.exists():
            subtotal = quote.subtotal
            tax_amount = quote.tax_amount
            total_amount = quote.total_amount
        else:
            # Fallback values
            from decimal import Decimal
            subtotal = Decimal('500000.00')
            tax_amount = subtotal * Decimal('0.10')
            total_amount = subtotal + tax_amount
        
        summary_data = [
            ["", "", "Subtotal:", f"₩{subtotal:,.2f}"],
            ["", "", "Tax (10%):", f"₩{tax_amount:,.2f}"],
            ["", "", "", ""],  # Spacer row
            ["", "", "TOTAL AMOUNT:", f"₩{total_amount:,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[8.5*cm, 2.5*cm, 3.5*cm, 3.5*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), self.font),
            ('FONTNAME', (0, -1), (-1, -1), self.font),
            ('FONTSIZE', (0, 0), (-1, -2), 11),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -2), self.text_color),
            
            # Total row highlighting
            ('BACKGROUND', (0, -1), (-1, -1), self.secondary_color),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            
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
        """Create enhanced terms and conditions section"""
        elements = []
        
        # Section title
        title_style = ParagraphStyle(
            'TermsTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName=self.font,
            textColor=self.primary_color,
            spaceAfter=10,
            spaceBefore=5
        )
        
        elements.append(Paragraph("TERMS & CONDITIONS", title_style))
        
        # Terms content with better formatting
        terms_content = """
        <font size="10" color="#2c3e50">
        <b>1. Quote Validity:</b> This quote is valid for 30 days from the issue date.<br/><br/>
        <b>2. Payment Terms:</b> Payment must be completed before service delivery begins.<br/><br/>
        <b>3. Service Delivery:</b> Estimated delivery time will be confirmed upon project acceptance.<br/><br/>
        <b>4. Modifications:</b> Any additional requirements or changes may result in revised pricing.<br/><br/>
        <b>5. Quality Assurance:</b> All services include quality review and client approval process.
        </font>
        """
        
        terms_table = Table([[Paragraph(terms_content, self.styles['Normal'])]], colWidths=[18*cm])
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
        """Create professional footer with signature area"""
        elements = []
        
        # Thank you message
        thank_you_style = ParagraphStyle(
            'ThankYou',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName=self.font,
            textColor=self.primary_color,
            alignment=TA_CENTER,
            spaceAfter=15
        )
        
        elements.append(Paragraph("Thank you for choosing Korea Translation & Interpretation Co., Ltd.", thank_you_style))
        
        # Signature section with enhanced styling
        signature_content = """
        <font size="11" color="#2c3e50">
        <b>To proceed with this quote, please sign below and return to us:</b>
        </font>
        """
        
        elements.append(Paragraph(signature_content, self.styles['Normal']))
        elements.append(Spacer(1, 0.4*cm))
        
        # Signature fields
        signature_data = [
            ["Client Signature", "Date", "KICAT Representative"],
            ["", "", ""],
            ["_" * 25, "_" * 15, "_" * 25],
            ["", "", ""],
            [f"Print Name: ________________", f"Date: ________", "Authorized by KICAT"]
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