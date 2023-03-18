from django.db import models

# Create your models here.


class ChatContent(models.Model):
    
    id = models.IntegerField(primary_key=True)
    role = models.CharField(verbose_name="角色",max_length=128)
    content = models.TextField(verbose_name="对话内容", max_length=8192)
    user_id = models.CharField(verbose_name="用户名", max_length=128)
    chat_model = models.CharField(verbose_name="对话模型", max_length=128)
    chat_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.role + " | " + self.content + " | " + self.user_id + " | " + self.chat_model + " | " + str(self.chat_time)

    
    class Meta:
        verbose_name = "对话内容"
        ordering = ["chat_time"]
        
        
if __name__ == "__main__":
    chat_content = ChatContent.objects.create(role="assistant", content="reply_content", user_id="to_user", chat_model="chat_model")
    chat_content.save()
    print(chat_content)
    
        