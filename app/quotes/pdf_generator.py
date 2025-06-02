from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime
import os


class QuotePDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.buffer = BytesIO()
        
        # Register Korean font with proper error handling
        try:
            # Try multiple CID fonts for better Korean support
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
            self.korean_font = 'HeiseiMin-W3'
            print("✅ Registered HeiseiMin-W3 font")
        except Exception as e:
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
                self.korean_font = 'HeiseiKakuGo-W5'
                print("✅ Registered HeiseiKakuGo-W5 font")
            except Exception as e2:
                try:
                    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
                    self.korean_font = 'STSong-Light'
                    print("✅ Registered STSong-Light font")
                except Exception as e3:
                    self.korean_font = 'Helvetica'
                    print(f"⚠️ Using Helvetica fallback. Errors: {e}, {e2}, {e3}")
                
        print(f"Using font: {self.korean_font}")
        
    def generate_quote_pdf(self, quote):
        """Generate a professional PDF quote for the given Quote object"""
        doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build PDF content
        story = []
        
        # Header with logo and quote info
        story.extend(self._create_header_with_quote_info(quote))
        story.append(Spacer(1, 0.5*cm))
        
        # Client information
        story.extend(self._create_client_info(quote))
        story.append(Spacer(1, 0.5*cm))
        
        # Service details table
        story.extend(self._create_service_table(quote))
        story.append(Spacer(1, 0.5*cm))
        
        # Terms and conditions
        story.extend(self._create_terms_and_conditions())
        story.append(Spacer(1, 1*cm))
        
        # Footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_content
    
    def _create_header_with_quote_info(self, quote):
        """Create header with company info and quote number"""
        elements = []
        
        # Company header with red background
        company_name = "한국통번역주식회사"
        quote_title = f"견적서 #{quote.id:04d}"
        
        header_data = [
            [company_name, quote_title]
        ]
        
        header_table = Table(header_data, colWidths=[12*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('FONTSIZE', (1, 0), (1, 0), 20),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(header_table)
        
        # Company details and quote details
        current_date = datetime.now()
        
        address = "서울특별시 강남구 도산대로 4200"
        phone = "+82-2-2022-0000"
        email = "info@kicat.co.kr"
        date_str = f"날짜: {current_date.strftime('%Y년 %m월 %d일')}"
        client_id = f"고객 ID: {quote.id:06d}"
        
        details_data = [
            [address, date_str],
            [phone, ""],
            [email, client_id]
        ]
        
        details_table = Table(details_data, colWidths=[9*cm, 9*cm])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(details_table)
        elements.append(Spacer(1, 0.5*cm))
        
        return elements
    
    def _create_client_info(self, quote):
        """Create client information section"""
        elements = []
        
        # Section header using Paragraph for better font control
        header_style = ParagraphStyle(
            'ClientHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            fontName=self.korean_font,
            textColor=colors.black
        )
        
        elements.append(Paragraph("고객 정보", header_style))
        
        # Client details
        company_info = f"회사: {quote.company}" if quote.company else "회사: -"
        name_info = f"담당자: {quote.name}" if quote.name else "담당자: -"
        phone_info = f"연락처: {quote.phone}" if quote.phone else "연락처: -"
        
        client_data = [
            [company_info, ""],
            [name_info, ""],
            [phone_info, ""]
        ]
        
        client_table = Table(client_data, colWidths=[18*cm])
        client_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(client_table)
        
        return elements
    
    def _create_service_table(self, quote):
        """Create service details table matching the design"""
        elements = []
        
        # Service table header
        header_data = [["설명", "수량", "가격", "총액"]]
        
        # Service items
        service_description = f"{quote.service_type.name}"
        if quote.message:
            service_description += f" - {quote.message[:30]}..."
        
        service_data = [
            [service_description, "1", "500,000원", "500,000원"]
        ]
        
        # Combine header and data
        table_data = header_data + service_data
        
        service_table = Table(table_data, colWidths=[8*cm, 3*cm, 3.5*cm, 3.5*cm])
        service_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            
            # Borders
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(service_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Summary section
        summary_data = [
            ["", "", "소계:", "500,000원"],
            ["", "", "부가세 (10%):", "50,000원"],
            ["", "", "총액:", "550,000원"]
        ]
        
        summary_table = Table(summary_data, colWidths=[8*cm, 3*cm, 3.5*cm, 3.5*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), self.korean_font),
            ('FONTNAME', (0, -1), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            
            # Total row highlighting
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            
            # Borders for summary area
            ('LINEBELOW', (2, -1), (-1, -1), 2, colors.black),
            ('LINEBEFORE', (2, 0), (2, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (2, 0), (-1, -1), 0.5, colors.grey),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(summary_table)
        
        return elements
    
    def _create_terms_and_conditions(self):
        """Create terms and conditions section"""
        elements = []
        
        header_style = ParagraphStyle(
            'TermsHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            fontName=self.korean_font
        )
        
        elements.append(Paragraph("약관 및 조건", header_style))
        
        terms_style = ParagraphStyle(
            'Terms',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=5,
            leftIndent=20,
            fontName=self.korean_font
        )
        
        terms = [
            "• 본 견적서는 30일간 유효합니다.",
            "• 결제는 서비스 제공 전에 완료되어야 합니다.",
            "• 추가 요구사항이 있을 경우 별도 협의가 필요합니다."
        ]
        
        for term in terms:
            elements.append(Paragraph(term, terms_style))
        
        return elements
    
    def _create_footer(self):
        """Create footer with signature section"""
        elements = []
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            fontName=self.korean_font,
            spaceAfter=20
        )
        
        elements.append(Paragraph("견적 승인", footer_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Signature section
        signature_data = [
            ["고객 서명", "날짜"],
            ["", ""],
            ["_" * 20, "_" * 20]
        ]
        
        signature_table = Table(signature_data, colWidths=[9*cm, 9*cm])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(signature_table)
        
        return elements


def generate_quote_pdf(quote):
    """Utility function to generate PDF for a quote"""
    generator = QuotePDFGenerator()
    pdf_content = generator.generate_quote_pdf(quote)
    
    # Create filename
    filename = f"견적서_{quote.id}_{quote.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Create ContentFile
    pdf_file = ContentFile(pdf_content, filename)
    
    return pdf_file 