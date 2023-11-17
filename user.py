import os
import re
import time
import response
import pyttsx3
import datetime
import tkinter as tk
from PIL import ImageGrab
import ttkbootstrap as ttk
from tkinter import messagebox


class Chat_UI:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)  
        self.engine.setProperty('voice', 'zh')

        self.chat_history_path = None
        self.files = None

        
        
    def Update_log(self):
        log_message = f"日期: 2023年11月15日\n--新增更换主题功能\n\n日期: 2023年11月17日\n--新增聊天记录功能.\n--新增语音功能" + " "*60
        messagebox.showinfo("Update_log", log_message)
        return

    def Report_bug(self):
        messagebox.showinfo("Report Bug", "Email: lwh20021104@gmail.com\n\nPlease report the bug through our support email." + " "*20)

    def Show_chat_history(self):

        def refresh_list():
            #print("正在刷新")
            insert_file_list()
            self.window.after(5000, refresh_list)


        def stop_refresh():
            if self.window.winfo_exists():
                self.window.after_cancel(refresh_list)
            
 
        def create_folder():
            self.chat_history_path = os.path.join(os.path.dirname(__file__), 'chat_history')
            if not os.path.exists(self.chat_history_path):
                os.makedirs(self.chat_history_path)
                #print(f"文件夹 '{self.chat_history_path}' 已创建。")
            
            return
        
        def insert_file_list():
            self.chat_history_path = os.path.join(os.path.dirname(__file__), 'chat_history')

            self.files = os.listdir(self.chat_history_path)
            self.files.reverse()

            self.file_list.delete(0, tk.END)

            for file in self.files:
                file_name = os.path.splitext(file)[0]
                self.file_list.insert(tk.END,file_name)

            return
        
        def insert_file_content(event):
            selected_file_index = self.file_list.curselection()
            if selected_file_index:
                file_index = int(selected_file_index[0])
                file_name = self.files[file_index]
                file_path = os.path.join(self.chat_history_path, file_name)

                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.file_text.delete(1.0, tk.END)
                    self.file_text.insert(tk.END, content)
            return
        
        def delete_file(event):
            selected_file_index = self.file_list.curselection()
            if selected_file_index:
                confirmation = messagebox.askokcancel("删除", "你确定要删除这个文件吗？")
                if confirmation:
                    file_index = int(selected_file_index[0])
                    file_name = self.files[file_index]
                    file_path = os.path.join(self.chat_history_path, file_name)
                    try:
                        os.remove(file_path)
                        del self.files[file_index]
                        self.file_list.delete(selected_file_index)
                        self.file_text.delete(1.0, tk.END)
                        messagebox.showinfo("成功", f"{os.path.splitext(file_name)[0]} 已删除。")
                    except FileNotFoundError:
                        messagebox.showerror("错误", f"未找到文件 {os.path.splitext(file_name)[0]}。")
            return
        
        self.window = tk.Tk()
        self.window.geometry('800x600+1000+100')
        self.window.title("聊天记录")

        paned_window = tk.PanedWindow(self.window, orient=tk.HORIZONTAL,sashwidth=2)
        self.file_list = tk.Listbox(paned_window)
        paned_window.add(self.file_list)
        self.file_text = tk.Text(paned_window)
        paned_window.add(self.file_text)

        paned_window.paneconfigure(self.file_list, minsize=200)
        paned_window.paneconfigure(self.file_text, minsize=400)

        paned_window.pack(fill=tk.BOTH, expand=True)

        create_folder()
        insert_file_list()
        self.window.after(1000, refresh_list)


        self.file_list.bind("<<ListboxSelect>>",lambda event:insert_file_content(event))
        self.file_list.bind("<Button-3>",lambda event:delete_file(event))
        self.file_list.bind("<Delete>",lambda event:delete_file(event))
        
        self.window.protocol("WM_DELETE_WINDOW", stop_refresh())
        
        self.window.mainloop()

    def Save_chat_history(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        chat_content = self.Chat_box.get("1.0", tk.END).strip()  # 获取并去除首尾空白

        if chat_content:  # 只有当有内容时才保存
            chat_history_path = os.path.join(os.path.dirname(__file__), 'chat_history')

            if not os.path.exists(chat_history_path):
                os.makedirs(chat_history_path)

            file_name = f"chat_{timestamp}.txt"
            file_path = os.path.join(chat_history_path, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(chat_content)

        self.root.destroy()
        
    def Save_chatimage(self):
        x = self.root.winfo_rootx() + self.Chat_box.winfo_x()
        y = self.root.winfo_rooty() + self.Chat_box.winfo_y()
        x1 = x + self.Chat_box.winfo_width()
        y1 = y + self.Chat_box.winfo_height()
        
        desktop_path = os.path.join(os.path.expanduser('~'),'Desktop')
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = "chat_" + current_datetime + ".png"
        file_path = os.path.join(desktop_path, file_name)
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

        messagebox.showinfo("Save", "聊天记录已成功保存到桌面，文件名为：" + file_name)

    def About_chat(self):
        messagebox.showinfo("About", "版本: 2.0.0\n日期: 2023-11-13\n学校: 上海大学" + " "*40)

    def Change_theme(self):
        theme_window = tk.Toplevel()
        theme_window.title("Theme")
        theme_window.geometry('300x130')

        theme_options = ["cosmo","morph","simplex",
                         "cerculean","darkly", "solar", 
                         "superhero","cyborg","vapor"]
        
        def apply_theme():
            selected_theme = theme_combobox.get()
            if selected_theme:
                ttk.Style().theme_use(selected_theme)

            return
        
        theme_label = tk.Label(theme_window, text="Choose Theme:")
        theme_label.pack()
        theme_combobox = ttk.Combobox(theme_window, values=theme_options, state="readonly")
        theme_combobox.pack()

        apply_button = tk.Label(theme_window, text="Apply")
        apply_button.pack(side=tk.LEFT, padx=2,expand=True)
        cancel_button = tk.Label(theme_window, text="Cancel")
        cancel_button.pack(side=tk.LEFT, padx=2,expand=True)

        apply_button.bind("<Button-1>",lambda e:apply_theme())
        cancel_button.bind("<Button-1>",lambda e:theme_window.destroy())

        theme_window.mainloop()
        
    def Clear_box(self):
        self.Chat_box.config(state=tk.NORMAL)
        self.Chat_box.delete(1.0,tk.END)
        self.Chat_box.config(state=tk.DISABLED)

    def Speak_voice(self):
        try:
            content = self.answer
            self.engine.say(content)
            self.speaking_flag = True
            self.engine.runAndWait()
            self.speaking_flag = False
        except Exception as e:
            print(f"Error in Speak_voice: {e}")

        return
    
    def Stop_speaking(self):
        if self.speaking_flag:
            self.engine.stop()
            self.speaking_flag = False

    def Input_get(self,event):

        User_input = self.Input_box.get()
        User_input_display ='👤' + "You:\n " + User_input + "\n"

        self.Chat_box.config(state=tk.NORMAL)
        self.Chat_box.insert(tk.END,User_input_display,'user_input_tag')
        self.Chat_box.insert(tk.END, "\n",'user_input_tag')

        self.Input_box.delete(0,tk.END)
        self.root.update()


        
        self.answer = response.get_answer(User_input)
        self.answer = re.sub('\n\s*\n', '\n', self.answer)
        answer_display ='🤖' + "Spark:\n "+ self.answer + "\n"

        self.Chat_box.insert(tk.END,answer_display,'answer_tag')
        self.Chat_box.insert(tk.END, "\n", 'answer_tag')
        self.Chat_box.config(state=tk.DISABLED)
        
    
    def user(self):
        self.root = ttk.Window(themename="cosmo")
        self.root.geometry('900x650')
        self.root.title("Chat")
        self.style = ttk.Style()
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Chat", menu=file_menu)
        preferences_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Preferences", menu=preferences_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)

        file_menu.add_command(label="About Chat",command=self.About_chat)
        file_menu.add_command(label="Check for Updates")
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.root.destroy)
        preferences_menu.add_command(label="Theme",command=self.Change_theme)
        help_menu.add_command(label="History",command=self.Show_chat_history)
        help_menu.add_command(label="Update Log",command=self.Update_log)
        help_menu.add_separator()
        help_menu.add_command(label="Report bug",command=self.Report_bug)

        
        Label_1 = tk.Label(self.root, text="Chat")
        Label_1.pack()

        self.Chat_box = tk.Text(self.root, height=12, width=48, state=tk.DISABLED)
        self.Chat_box.pack(expand=True, fill="both")
        self.Chat_box.tag_config('user_input_tag', foreground='blue')
        self.Chat_box.tag_config('answer_tag', foreground='green')
        self.Chat_box.tag_config('wait_tag', foreground='green')

        Frame = tk.Frame(self.root)
        Frame.pack(side=tk.LEFT, expand=True, fill="both", pady=15, padx=20)

        Label_2 = tk.Label(Frame, text="请输入:")
        Label_2.pack(side=tk.LEFT, expand=True, fill="both")

        self.Input_box = tk.Entry(Frame, width=50)
        self.Input_box.pack(side=tk.LEFT, expand=True, fill="both")


        clear = tk.Label(Frame, text="\U0001F504",cursor="hand2")
        clear.pack(side=tk.LEFT, expand=True, fill="both")
        save = tk.Label(Frame, text="🌄",cursor="hand2")
        save.pack(side=tk.LEFT, expand=True, fill="both")
        
        speak = tk.Label(Frame, text="🎤")
        speak.pack(side=tk.LEFT, expand=True, fill="both")

        self.Input_box.bind("<Return>",lambda event: self.Input_get(event))
        clear.bind("<Button-1>",lambda e:self.Clear_box())
        save.bind("<Button-1>",lambda e:self.Save_chatimage())
        speak.bind("<Button-1>",lambda e:self.Speak_voice())

        self.root.protocol("WM_DELETE_WINDOW", self.Save_chat_history)
        self.root.mainloop()

if __name__ == "__main__":
    chat_ui = Chat_UI()
    chat_ui.user()