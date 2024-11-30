from tkinter import *
from tkinter import font,filedialog
from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.extra import ExtraExtension
from emoji import EmojiExtension
from tkhtmlview import HTMLLabel
from tkinter import messagebox as mbox
import webbrowser
class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.myfont=font.Font(family='KaiTi',size=14)
        self.init_window()
    def init_window(self):
        self.master.title("markdown编辑器")
        self.pack(fill=BOTH, expand=1)
        self.inputeditor = Text(self,width="1",font=self.myfont)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)
        
        self.scrollbar = Scrollbar(self.inputeditor)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.inputeditor.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.inputeditor.yview)
        
        self.outputbox = HTMLLabel(self, width="1", background="white", html="<h1>markdown</h1>")  
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)  
        self.outputbox.fit_height()
        
        self.word_count_label = Label(self, text="", font=self.myfont)
        self.word_count_label.pack(side=BOTTOM)
        
        self.bold_button = Button(self, text="加粗", command=self.bold_selected_text)
        self.bold_button.pack(side=TOP)
        self.bold_button1 = Button(self, text="斜体", command=self.italics_selected_text)
        self.bold_button1.pack(side=TOP)
        
        self.inputeditor.bind("<KeyRelease>", self.onInputChange)
        self.inputeditor.bind("<<Modified>>", self.onInputChange) 
        self.inputeditor.bind("<KeyRelease>", self.onInputChange)
        self.inputeditor.bind("<MouseWheel>", self.onMouseWheel) 
        
        self.mainmenu = Menu(self)  
        self.filemenu = Menu(self.mainmenu)  
        self.helpmenu = Menu(self.mainmenu)
        
        self.filemenu.add_command(label="打开", command=self.openfile)  
        self.filemenu.add_command(label="另存为", command=self.savefile)  
        self.filemenu.add_separator()
        self.filemenu.add_command(label="预览", command=self.preview_markdown)
        self.filemenu.add_separator() 
        self.filemenu.add_command(label="退出", command=self.quit)  
        
        self.insertmenu = Menu(self.filemenu)  
        self.insertmenu.add_command(label="图片", command=self.insert_image)  
        self.insertmenu.add_command(label="代码", command=self.insert_code)  
        self.insertmenu.add_command(label="表情符号", command=self.insert_emoji)  
        
        self.mainmenu.add_cascade(label="文件", menu=self.filemenu)  
        self.mainmenu.add_cascade(label="插入", menu=self.insertmenu)
        self.mainmenu.add_cascade(label="帮助", menu=self.helpmenu)
        self.helpmenu.add_command(label="用户手册", command=self.about)
        
        self.master.config(menu=self.mainmenu)  
    def about(self):
        mbox.showinfo("帮助", "1.用户可以点击打开按钮打开一个markdown文件\n2.用户可以点击另存为按钮将当前编辑的markdown文件保存为本地文件\n3.用户可以点击预览按钮在浏览器中预览当前编辑的markdown文件\n4.用户可以点击退出按钮退出程序\n5.用户可以点击加粗按钮将选中的文字加粗\n6.用户可以点击斜体按钮将选中的文字斜体\n7.用户可以点击图片按钮插入一张图片\n8.用户可以点击代码按钮插入一段代码\n9.用户可以点击表情符号按钮插入一个表情符号\n\n最终解释权归第八组所有")
    def onInputChange(self, event):
        markdownText = self.inputeditor.get("1.0", END)
        markdownText2 = self.outputbox.get("1.0", END)
        # 去除可能存在的换行符等空白字符，只统计有效字符个数
        clean_text = markdownText.strip()
        clean_text2 = markdownText2.strip()
        # 按照每个字符进行统计，这里直接使用len函数获取字符个数
        word_count = len(clean_text)
        word_count1 = len(clean_text2)
        # 更新字数统计Label的文本内容
        self.word_count_label.config(text=f"输入字节{word_count}      输出字数{word_count1}")

        # 更新字数统计标签的位置，确保它始终在底部
        self.word_count_label.place(x=0, y=self.winfo_height() - self.word_count_label.winfo_height(), relwidth=1)
        self.inputeditor.edit_modified(0)  
        markdownText = self.inputeditor.get("1.0", END) 
        html = markdown(markdownText, extensions=[FencedCodeExtension(), ExtraExtension(), EmojiExtension()])
        html = f"<link rel='stylesheet' type='text/css' href='styles.css'>{html}"
        self.outputbox.set_html(html)
    def openfile(self):  
        openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),("Text File", "*.txt")))  
        if openfilename:  
            try:  
                self.inputeditor.delete(1.0, END)  
                self.inputeditor.insert(END , open(openfilename).read())  
            except:  
                mbox.showerror("打开选定文件时出错 " , "您选择的文件：{}无法打开!".format(openfilename))
    def savefile(self):  
        filedata = self.inputeditor.get("1.0" , END)  
        savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"),("Text File", "*.txt")) , title="保存 Markdown 文件")  
        if savefilename:  
            try:  
                f = open(savefilename , "w")  
                f.write(filedata)  
            except:  
                mbox.showerror("保存文件错误" , "文件: {} 保存错误！".format(savefilename))  
    def onMouseWheel(self, event):
        input_scroll = int(-1 * (event.delta / 120))
        self.inputeditor.yview_scroll(input_scroll, "units")  
        input_pos = self.inputeditor.yview()
        output_pos = self.outputbox.yview()
        output_scroll = (input_pos[0] * (self.outputbox.winfo_height() / self.inputeditor.winfo_height())) - output_pos[0]
        self.outputbox.yview_scroll(int(output_scroll * 120), "units")  
    def insert_image(self):
        popup = Toplevel(self)
        popup.title("插入图片")
        popup.geometry("300x150")
        label = Label(popup, text="请输入图片链接:")
        label.pack(pady=10)
        entry = Entry(popup, width=30)
        entry.pack(pady=10)
        button_frame = Frame(popup)
        button_frame.pack(pady=10)
        btn_confirm = Button(button_frame, text="确认", command=lambda: self.insert_at_cursor(f"![图片]({entry.get()})") or popup.destroy())
        btn_confirm.pack(side=LEFT, padx=5)
        btn_cancel = Button(button_frame, text="取消", command=popup.destroy)
        btn_cancel.pack(side=LEFT, padx=5)
    def insert_code(self):
        popup = Toplevel(self)
        popup.title("插入代码")
        popup.geometry("300x500")

        # 创建语言选择下拉菜单
        languages = ["python","javascript", "cpp", "html", "css"]
        language_var = StringVar(popup)
        language_var.set(languages[0])  # 默认选择第一个语言
        language_label = Label(popup, text="选择编程语言:")
        language_label.pack(pady=5)
        language_menu = OptionMenu(popup, language_var, *languages)
        language_menu.pack(pady=5)
        # 创建代码输入框
        code_label = Label(popup, text="输入代码:")
        code_label.pack(pady=5)
        code_entry = Text(popup, width=40,height=20)
        code_entry.pack(pady=5)

        # 创建确认和取消按钮
        button_frame = Frame(popup)
        button_frame.pack(pady=10)
        
        def insert_code_block():
            language = language_var.get()
            code = code_entry.get("1.0", END)
            formatted_code = f"```{language}\n{code}\n```"
            self.insert_at_cursor(formatted_code)
            popup.destroy()

        btn_confirm = Button(button_frame, text="确认", command=insert_code_block)
        btn_confirm.pack(side=LEFT, padx=5)
        btn_cancel = Button(button_frame, text="取消", command=popup.destroy)
        btn_cancel.pack(side=LEFT, padx=5)


    def insert_at_cursor(self, text):
        pos = self.inputeditor.index(INSERT)  
        self.inputeditor.insert(pos, text)  
        self.inputeditor.focus()  

    def insert_emoji(self):
        popup = Toplevel(self)
        popup.title("插入表情符号")
        popup.geometry("300x200")
        
        frame1 = Frame(popup)
        frame1.pack(pady=5)
        frame2 = Frame(popup)
        frame2.pack(pady=5)
        frame3 = Frame(popup)
        frame3.pack(pady=5)
        emoji_list1 = ["😀", "😂", "😍","🥰","🤪","😘","🤗"]
        emoji_list2 = ["😢", "👍","🥵","🥶","🥺","💩","🤓"]
        emoji_list3 = ["🎉", "🤬", "👆","👉","👈","🤡","🤣"]
        for emoji in emoji_list1:
            btn = Button(frame1, text=emoji, command=lambda e=emoji: self.insert_at_cursor(e))
            btn.pack(side=LEFT, padx=5)
        for emoji in emoji_list2:
            btn = Button(frame2, text=emoji, command=lambda e=emoji: self.insert_at_cursor(e))
            btn.pack(side=LEFT, padx=5)
        for emoji in emoji_list3:
            btn = Button(frame3, text=emoji, command=lambda e=emoji: self.insert_at_cursor(e))
            btn.pack(side=LEFT, padx=5)
    def preview_markdown(self):  
        markdownText = self.inputeditor.get("1.0", END)
        html = markdown(markdownText, extensions=[FencedCodeExtension(), ExtraExtension(), EmojiExtension()])
        html = f"<link rel='stylesheet' type='text/css' href='styles.css'>{html}"
        html = f"""
        <link rel='stylesheet' type='text/css' href='styles.css'>
        {html}
        """
        with open("preview.html", "w", encoding="utf-8") as f:  
            f.write(html)
        
        webbrowser.open("preview.html")  
    def bold_selected_text(self):
        try:
            start_index = self.inputeditor.index("sel.first")
            end_index = self.inputeditor.index("sel.last")
            selected_text = self.inputeditor.get(start_index, end_index)
            self.inputeditor.delete(start_index, end_index)
            self.inputeditor.insert(start_index, f"**{selected_text}**")

            # 插入新文本后，更新光标的位置，使其位于插入后的文本之后
            new_index = self.inputeditor.index(f"{start_index}+{len(selected_text)}c")
            self.inputeditor.mark_set("insert", new_index)
        except:
            mbox.showerror("加粗操作错误", "请先选中要加粗的文字！")
    def italics_selected_text(self):
        try:
            start_index = self.inputeditor.index("sel.first")
            end_index = self.inputeditor.index("sel.last")
            selected_text = self.inputeditor.get(start_index, end_index)
            self.inputeditor.delete(start_index, end_index)
            self.inputeditor.insert(start_index, f"*{selected_text}*")

            # 插入新文本后，更新光标的位置，使其位于插入后的文本之后
            new_index = self.inputeditor.index(f"{start_index}+{len(selected_text)}c")
            self.inputeditor.mark_set("insert", new_index)

        except:
            mbox.showerror("斜体操作错误", "请先选中要斜体的文字！")
if __name__=='__main__':
    root = Tk()  
    root.geometry("800x600")  
    app = Window(root)  
    app.mainloop()  