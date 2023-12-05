import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

import response
import os
import re
import sys
import datetime
import subprocess


class Chat_UI(ttk.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        self.title("Chat")
        
        
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        self.frames = {}

        
        for F in (user_UI, history_UI):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        
        self.show_frame(user_UI)

        
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        
        chat_menu = tk.Menu(menu_bar, tearoff=0)
        self.config(menu=menu_bar)

        
        chat_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Chat", menu=chat_menu)
        chat_menu.add_command(label="About Chat",command=lambda: self.About_chat())
        chat_menu.add_command(label="Check for Updates",command=lambda: self.Check_for_updates())
        chat_menu.add_command(label="Illustrate",command=lambda: self.Illustrate())
        chat_menu.add_separator()
        chat_menu.add_command(label="Exit",command=self.destroy)

        
        preferences_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Preferences", menu=preferences_menu)
        preferences_menu.add_command(label="Theme", command=lambda: self.Change_theme())
        preferences_menu.add_separator()
        preferences_menu.add_command(label="Restart Chat", command=lambda: self.Restart_chat())

        
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut                Ctrl+X")
        edit_menu.add_command(label="Copy             Ctrl+C")
        edit_menu.add_command(label="Paste             Ctrl+V")
        edit_menu.add_command(label="Select all      Ctrl+A")


        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Chat",command=lambda: self.show_frame(user_UI))
        help_menu.add_command(label="History",command=lambda: self.show_frame(history_UI))
        help_menu.add_separator()
        help_menu.add_command(label="Update Log",command=lambda: self.Update_log())
        help_menu.add_command(label="Report bug",command=lambda: self.Report_bug())

        self.protocol("WM_DELETE_WINDOW", self.on_close)
          
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def Update_log(self):
        log_message = f"日期: 2023年11月15日\n--新增更换主题功能\n\n日期: 2023年11月17日\n--新增聊天记录功能.\n\n日期: 2023年12月5日\n--界面优化" + " "*60
        messagebox.showinfo("Update_log", log_message)
        return

    def Report_bug(self):
        messagebox.showinfo("Report Bug", "Email: lwh20021104@gmail.com\n\nPlease report the bug through our support email." + " "*20)

    def About_chat(self):
        messagebox.showinfo("About", "版本: 3.0.0\n日期: 2023-11-13\n学校: 上海大学" + " "*40)

    def Illustrate(self):
        messagebox.showinfo("Illustrate", "ChatGPT can make mistakes. \nConsider checking important information." + " "*10)
        

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

    def Check_for_updates(self):
        current_version = "3.0.0"
        latest_version = self.get_latest_version_from_server()

        if latest_version > current_version:
            messagebox.showinfo("更新提示", f"发现新版本 ({latest_version})，请及时更新。")
        else:
            messagebox.showinfo("已是最新", "你正在使用最新版本。")

    def get_latest_version_from_server(self):

        return "3.0.0"

    def Restart_chat(self):
        self.destroy()

        python_executable = sys.executable
        subprocess.Popen([python_executable] + sys.argv)

    def on_close(self):
        # 在窗口关闭时调用 Save_chat_history 方法
        self.frames[user_UI].Save_chat_history()
        self.destroy()


class history_UI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.chat_history_path = None
        self.files = None

        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL,sashwidth=2)
        self.file_list = tk.Listbox(paned_window)
        paned_window.add(self.file_list)
        self.file_text = tk.Text(paned_window)
        paned_window.add(self.file_text)

        paned_window.paneconfigure(self.file_list, minsize=200)
        paned_window.paneconfigure(self.file_text, minsize=400)

        paned_window.pack(fill=tk.BOTH, expand=True)

        self.create_folder()
        self.insert_file_list()
        self.after(1000,self.refresh_list)

        self.file_list.bind("<<ListboxSelect>>",lambda event:self.insert_file_content(event))
        self.file_list.bind("<Button-3>",lambda event:self.delete_file(event))
    
    def insert_file_list(self):
        self.chat_history_path = os.path.join(os.path.dirname(__file__), 'chat_history')
        self.files = os.listdir(self.chat_history_path)

        self.files.reverse()

        self.file_list.delete(0, tk.END)

        for file in self.files:
            file_name = os.path.splitext(file)[0]
            self.file_list.insert(tk.END,file_name)

        return
    
    def refresh_list(self):
        self.insert_file_list()
        self.after(5000, self.refresh_list)
    
    def insert_file_content(self,event):
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

    def delete_file(self,event):
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

    def create_folder(self):
        self.chat_history_path = os.path.join(os.path.dirname(__file__), 'chat_history')
        if not os.path.exists(self.chat_history_path):
            os.makedirs(self.chat_history_path)
        
        return

class user_UI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Label_1 = tk.Label(self, text="Chat")
        Label_1.pack()

        self.Chat_box = tk.Text(self, height=12, width=48, state=tk.DISABLED)
        self.Chat_box.pack(expand=True, fill="both")
        self.Chat_box.tag_config('user_input_tag', foreground='blue')
        self.Chat_box.tag_config('answer_tag', foreground='green')

        Frame = tk.Frame(self)
        Frame.pack(side=tk.LEFT, expand=True, fill="both", pady=15, padx=20)

        Label_2 = tk.Label(Frame, text="请输入:")
        Label_2.pack(side=tk.LEFT, expand=True, fill="both")

        self.Input_box = tk.Entry(Frame, width=50)
        self.Input_box.pack(side=tk.LEFT, expand=True, fill="both")

        clear = tk.Label(Frame, text="\U0001F504",cursor="hand2")
        clear.pack(side=tk.LEFT, expand=True, fill="both")

        self.Input_box.bind("<Return>",lambda event: self.Input_get(event))
        clear.bind("<Button-1>",lambda e:self.Clear_box())

        
    def Input_get(self,event):

        User_input = self.Input_box.get()
        User_input_display ='👤' + "You:\n " + User_input + "\n"
        Chat_input_display ='🤖' + "Spark:\n "

        self.Chat_box.config(state=tk.NORMAL)
        self.Chat_box.insert(tk.END,User_input_display,'user_input_tag')
        self.Chat_box.insert(tk.END, "\n",'user_input_tag')
        self.Chat_box.insert(tk.END,Chat_input_display)
        self.Input_box.delete(0,tk.END)
        self.update()
        
        self.answer = response.get_answer(User_input)
        self.answer = re.sub('\n\s*\n', '\n', self.answer)

        self.type_writer_effect(self.answer,  delay=50)

        self.Chat_box.insert(tk.END, "\n")
        self.Chat_box.config(state=tk.DISABLED)
        
    def type_writer_effect(self, text, delay=50, index=0):
        if index < len(text):
            
            self.Chat_box.config(state=tk.NORMAL)
            self.Chat_box.insert(tk.END, text[index])
            self.Chat_box.config(state=tk.DISABLED)
            self.Chat_box.yview(tk.END)  

            
            self.after(delay, lambda: self.type_writer_effect(text, delay, index + 1))
        else:
            
            self.Chat_box.config(state=tk.NORMAL)
            self.Chat_box.insert(tk.END, "\n\n")
            self.Chat_box.config(state=tk.DISABLED)
            self.Chat_box.yview(tk.END)  
            
            pass

    def Clear_box(self):
        self.Chat_box.config(state=tk.NORMAL)
        self.Chat_box.delete(1.0,tk.END)
        self.Chat_box.config(state=tk.DISABLED)

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
   

if __name__ == "__main__":
    app = Chat_UI(themename="cosmo")
    app.geometry("900x650")
    app.mainloop()