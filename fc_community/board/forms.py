from django import forms


class BoardForm(forms.Form):
    title = forms.CharField(max_length=128, label="제목",
                            error_messages={
                                  'required': '제목을 입력해주세요'
                            })
    contents = forms.CharField(widget=forms.Textarea, label="내용",
                               error_messages={
                                   'required': '내용을 입력해주세요'
                               })
    # 빈칸 검증을 제외한 검증은 따로 필요없을 것 같으니 clean 함수는 없앤다.
