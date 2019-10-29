from django.db import models

class Board(models.Model):
	title = models.CharField(max_length=128, verbose_name='제목')
	contents = models.TextField(verbose_name='내용')
    # 외래키로 id로 연결한다. 이 때, on_delete 라는 옵션을 꼭 넣어줘야한다. CASCADE 옵션으로 연쇄적으로 삭제된다.
	writer = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='작성자')

	tags = models.ManyToManyField('tag.Tag', verbose_name='태그')
	registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

	def __str__(self):
		return self.title
	class Meta:
		db_table = 'fastcampus_board'
		verbose_name = '패스트캠퍼스 게시글'
		verbose_name_plural = '패스트캠퍼스 게시글들'
