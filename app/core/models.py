from django.db import models
from django.core.validators import FileExtensionValidator

class Award(models.Model):
    """Model for awards, certifications, and academic conferences"""
    
    title = models.CharField(
        max_length=200,
        verbose_name="수상/행사명",
        help_text="수상명 또는 학술대회명을 입력하세요"
    )
    
    description = models.TextField(
        verbose_name="상세 설명",
        help_text="수상 내용 또는 행사에 대한 자세한 설명을 입력하세요"
    )
    
    date = models.DateField(
        verbose_name="수상/개최일",
        help_text="수상일 또는 행사 개최일을 입력하세요"
    )
    
    location = models.CharField(
        max_length=200,
        verbose_name="장소",
        help_text="수상 장소 또는 행사 개최지를 입력하세요"
    )
    
    image = models.ImageField(
        upload_to='awards/',
        verbose_name="대표 이미지",
        help_text="수상 또는 행사와 관련된 이미지를 업로드하세요",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    short_description = models.CharField(
        max_length=100,
        verbose_name="간략 설명",
        help_text="카드에 표시될 간략한 설명 (예: 2022년 한국번역가협회)",
        blank=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성화",
        help_text="체크 해제 시 웹사이트에서 숨겨집니다"
    )
    
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="표시 순서",
        help_text="낮은 숫자가 먼저 표시됩니다"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "수상 및 학술대회"
        verbose_name_plural = "수상 및 학술대회"
        ordering = ['display_order', '-date']
    
    def __str__(self):
        return f"{self.title} ({self.date.year}년)"
    
    def get_formatted_date(self):
        """Return formatted date string for display"""
        return self.date.strftime("%Y년 %m월 %d일")
    
    def get_year_location(self):
        """Return year and location for card subtitle"""
        return f"{self.date.year}년 {self.location}"
