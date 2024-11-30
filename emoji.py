from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import re

class EmojiExtension(Extension):
    """Markdown 的 emoji 表情扩展类"""
    def __init__(self, **kwargs):
        # 配置默认的 emoji 映射字典
        self.config = {
            'emoji_index': [
                {
                    'smile': '😊',
                    'laugh': '😂',
                    'wink': '😉',
                    'heart': '❤️',
                    'thumbsup': '👍',
                    'star': '⭐',
                    'glasses':'🤓',
                    'angry': '🤬',
                    'clown': '🤡',
                    'laugh_lean': '🤣',
                    'hot': '🥵',
                    'cold': '🥶',
                    'pleading': '🥺',
                    'shit': '💩',
                    'finger_up': '👆',
                    'finger_left': '👈',
                    'finger_right': '👉',
                    'heart_eyes': '🥰',
                    'crazy': '🤪',
                    'kiss': '😘',
                    'hug': '🤗',
                },
                'Default emoji mappings'  # emoji 映射的描述
            ]
        }
        super(EmojiExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """扩展 Markdown 语法，添加 emoji 处理功能"""
        # 获取 emoji 映射字典
        emoji_index = self.getConfig('emoji_index')
        # 定义 emoji 的正则表达式模式，匹配 :emoji_code: 格式
        emoji_pattern = r':([a-z0-9+\-_]+):'
        # 创建 emoji 处理器实例
        emoji_processor = EmojiInlineProcessor(emoji_pattern, emoji_index)
        # 注册 emoji 处理器，优先级为 75
        md.inlinePatterns.register(emoji_processor, 'emoji', 75)

class EmojiInlineProcessor(InlineProcessor):
    """Emoji 内联处理器类"""
    def __init__(self, pattern, emoji_index):
        super(EmojiInlineProcessor, self).__init__(pattern)
        self.emoji_index = emoji_index

    def handleMatch(self, m, data):
        """处理匹配到的 emoji 代码
        
        Args:
            m: 正则表达式匹配对象
            data: 输入文本数据
            
        Returns:
            tuple: (emoji字符, 开始位置, 结束位置) 或 (None, None, None)
        """
        # 获取匹配到的 emoji 代码
        emoji_code = m.group(1)
        # 检查 emoji 代码是否存在于映射字典中
        if emoji_code in self.emoji_index:
            emoji = self.emoji_index[emoji_code]
            return emoji, m.start(0), m.end(0)
        else:
            return None, None, None

def makeExtension(**kwargs):
    """创建扩展的工厂函数"""
    return EmojiExtension(**kwargs)
