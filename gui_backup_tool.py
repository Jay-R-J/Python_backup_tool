#!/usr/bin/env python3
"""
项目自动备份工具 - 图形界面版本
作者：Jay
版本：1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import threading
import datetime
from backup_tool import ProjectBackupTool
from pathlib import Path
import sys

class BackupToolGUI:
    def __init__(self, root):
        """
        初始化图形界面
        """
        self.root = root
        self.root.title("项目备份工具")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # 设置窗口图标（如果有）
        # try:
        #     self.root.iconbitmap("backup_icon.ico")
        # except:
        #     pass
        
        # 初始化备份工具
        self.backup_tool = ProjectBackupTool()
        
        # 设置现代化样式
        self.style = ttk.Style()
        self.setup_style()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面组件
        self.create_widgets()
        
        # 加载备份列表
        self.load_backups()
    
    def setup_style(self):
        """
        设置现代化样式
        """
        # 使用系统主题
        self.style.theme_use('clam')
        
        # 自定义颜色
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333333")
        self.style.configure("TLabelframe", background="#f0f0f0", foreground="#333333")
        self.style.configure("TLabelframe.Label", background="#f0f0f0", foreground="#333333", font=('Arial', 10, 'bold'))
        
        # 按钮样式
        self.style.configure("TButton", background="#4CAF50", foreground="white", padding=5, font=('Arial', 9))
        self.style.map("TButton", 
                     background=[('active', '#45a049'), ('disabled', '#cccccc')],
                     foreground=[('disabled', '#666666')])
        
        # 强调按钮样式
        self.style.configure("Accent.TButton", background="#2196F3", foreground="white")
        self.style.map("Accent.TButton", 
                     background=[('active', '#0b7dda'), ('disabled', '#cccccc')])
        
        # 危险按钮样式
        self.style.configure("Danger.TButton", background="#f44336", foreground="white")
        self.style.map("Danger.TButton", 
                     background=[('active', '#da190b'), ('disabled', '#cccccc')])
        
        # 标题样式
        self.style.configure("Title.TLabel", font=('Arial', 16, 'bold'), background="#f0f0f0", foreground="#2196F3")
        
        # 状态标签样式
        self.style.configure("Status.TLabel", font=('Arial', 9), background="#e0e0e0", foreground="#666666")
        
        # 树状图样式
        self.style.configure("Treeview", 
                           background="white",
                           foreground="#333333",
                           rowheight=25,
                           fieldbackground="white",
                           font=('Arial', 9))
        self.style.configure("Treeview.Heading", 
                           background="#2196F3",
                           foreground="white",
                           font=('Arial', 10, 'bold'),
                           padding=6)
        self.style.map("Treeview.Heading", 
                     background=[('active', '#0b7dda')])
        self.style.map("Treeview", 
                     background=[('selected', '#e3f2fd')],
                     foreground=[('selected', '#0d47a1')])
        
        # 滚动条样式
        self.style.configure("Vertical.TScrollbar", background="#e0e0e0")
        self.style.map("Vertical.TScrollbar", 
                     background=[('active', '#bdbdbd')])
        
    def create_widgets(self):
        """
        创建界面组件
        """
        # 标题区域
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        # 标题标签
        title_label = ttk.Label(title_frame, text="项目备份管理工具", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=10)
        
        # 版本信息
        version_label = ttk.Label(title_frame, text="v1.0", font=('Arial', 8), foreground="#666666")
        version_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 项目信息框架
        info_frame = ttk.LabelFrame(self.main_frame, text="备份设置", padding="15")
        info_frame.pack(fill=tk.X, pady=5)
        
        # 第一行：源目录选择
        source_frame = ttk.Frame(info_frame)
        source_frame.pack(fill=tk.X, pady=5)
        
        source_dir_label = ttk.Label(source_frame, text="要备份的目录: ", width=12, font=('Arial', 9, 'bold'))
        source_dir_label.pack(side=tk.LEFT, padx=10, pady=2, anchor=tk.CENTER)
        
        self.source_dir_var = tk.StringVar()
        self.source_dir_var.set(str(self.backup_tool.source_dir))
        
        source_dir_entry = ttk.Entry(source_frame, textvariable=self.source_dir_var, width=60, font=('Arial', 9))
        source_dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, pady=2)
        
        select_source_btn = ttk.Button(source_frame, text="浏览...", command=self.select_source_dir, width=10)
        select_source_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 第二行：备份目录选择
        backup_frame = ttk.Frame(info_frame)
        backup_frame.pack(fill=tk.X, pady=5)
        
        backup_dir_label = ttk.Label(backup_frame, text="备份保存位置: ", width=12, font=('Arial', 9, 'bold'))
        backup_dir_label.pack(side=tk.LEFT, padx=10, pady=2, anchor=tk.CENTER)
        
        self.backup_dir_var = tk.StringVar()
        self.backup_dir_var.set(str(self.backup_tool.backup_dir))
        
        backup_dir_entry = ttk.Entry(backup_frame, textvariable=self.backup_dir_var, width=60, font=('Arial', 9))
        backup_dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, pady=2)
        
        select_backup_btn = ttk.Button(backup_frame, text="浏览...", command=self.select_backup_dir, width=10)
        select_backup_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 第三行：备份数量
        self.backup_count_var = tk.StringVar()
        backup_count_frame = ttk.Frame(info_frame)
        backup_count_frame.pack(fill=tk.X, pady=5)
        
        backup_count_label = ttk.Label(backup_count_frame, textvariable=self.backup_count_var, font=('Arial', 9, 'bold'), foreground="#2196F3")
        backup_count_label.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # 操作按钮框架
        button_frame = ttk.Frame(self.main_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=5)
        
        # 按钮容器，居中显示
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(anchor=tk.CENTER)
        
        # 创建备份按钮（强调样式）
        create_btn = ttk.Button(btn_container, text="创建备份", 
                               command=self.create_backup, style="Accent.TButton", width=12)
        create_btn.pack(side=tk.LEFT, padx=8, pady=5)
        
        # 恢复按钮
        restore_btn = ttk.Button(btn_container, text="恢复备份", 
                                command=self.restore_backup, width=12)
        restore_btn.pack(side=tk.LEFT, padx=8, pady=5)
        
        # 删除按钮（危险样式）
        delete_btn = ttk.Button(btn_container, text="删除备份", 
                               command=self.delete_backup, style="Danger.TButton", width=12)
        delete_btn.pack(side=tk.LEFT, padx=8, pady=5)
        
        # 刷新按钮
        refresh_btn = ttk.Button(btn_container, text="刷新列表", 
                               command=self.load_backups, width=12)
        refresh_btn.pack(side=tk.LEFT, padx=8, pady=5)
        
        # 备份列表框架
        list_frame = ttk.LabelFrame(self.main_frame, text="备份列表", padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 列表视图
        columns = ("id", "timestamp", "comment", "type")
        self.backup_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # 设置列宽和标题
        self.backup_tree.heading("id", text="版本ID", anchor=tk.CENTER)
        self.backup_tree.heading("timestamp", text="备份时间", anchor=tk.CENTER)
        self.backup_tree.heading("comment", text="注释", anchor=tk.CENTER)
        self.backup_tree.heading("type", text="类型", anchor=tk.CENTER)
        
        self.backup_tree.column("id", width=120, anchor=tk.CENTER, minwidth=100)
        self.backup_tree.column("timestamp", width=200, anchor=tk.CENTER, minwidth=180)
        self.backup_tree.column("comment", width=350, anchor=tk.CENTER, minwidth=300)
        self.backup_tree.column("type", width=100, anchor=tk.CENTER, minwidth=80)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                  command=self.backup_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, 
                                  command=self.backup_tree.xview)
        self.backup_tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        # 放置树状图和滚动条
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 添加网格线
        self.backup_tree.configure(displaycolumns="#all")
        
        # 双击事件
        self.backup_tree.bind("<Double-1>", self.on_double_click)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, 
                              font=('Arial', 9), background="#e0e0e0", 
                              foreground="#333333", padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def select_source_dir(self):
        """
        选择要备份的源目录
        """
        # 打开目录选择对话框
        selected_dir = filedialog.askdirectory(title="选择要备份的目录")
        if selected_dir:
            try:
                # 设置新的源目录
                self.backup_tool.set_source_dir(selected_dir)
                # 更新界面显示
                self.source_dir_var.set(str(self.backup_tool.source_dir))
                # 重新加载备份列表
                self.load_backups()
                messagebox.showinfo("成功", f"要备份的目录已更新为: {selected_dir}")
            except Exception as e:
                messagebox.showerror("错误", f"更新源目录失败: {e}")
    
    def select_backup_dir(self):
        """
        选择备份保存位置
        """
        # 打开目录选择对话框
        selected_dir = filedialog.askdirectory(title="选择备份保存位置")
        if selected_dir:
            try:
                # 设置新的备份目录
                self.backup_tool.set_backup_dir(selected_dir)
                # 更新界面显示
                self.backup_dir_var.set(str(self.backup_tool.backup_dir))
                # 重新加载备份列表
                self.load_backups()
                messagebox.showinfo("成功", f"备份保存位置已更新为: {selected_dir}")
            except Exception as e:
                messagebox.showerror("错误", f"更新备份目录失败: {e}")
    
    def load_backups(self):
        """
        加载备份列表
        """
        # 清空现有数据
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        # 获取备份列表
        backups = self.backup_tool.list_backups()
        
        # 更新备份数量
        self.backup_count_var.set(f"备份数量: {len(backups)}")
        
        # 添加到树状图
        for backup in backups:
            # 格式化时间
            timestamp = datetime.datetime.fromisoformat(backup["timestamp"])
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            # 备份类型
            backup_type = "压缩" if backup.get("compression", True) else "文件夹"
            
            self.backup_tree.insert("", tk.END, values=(
                backup["id"],
                formatted_time,
                backup["comment"],
                backup_type
            ))
        
        self.status_var.set("备份列表已更新")
    
    def create_backup(self):
        """
        创建备份
        """
        # 获取注释
        comment = simpledialog.askstring("创建备份", "请输入备份注释（可选）:")
        if comment is None:
            return
        
        # 开始备份线程
        def backup_thread():
            self.status_var.set("正在创建备份...")
            result = self.backup_tool.create_backup(comment)
            if result:
                messagebox.showinfo("备份成功", f"备份已创建: {result['id']}")
                self.load_backups()
            else:
                messagebox.showerror("备份失败", "创建备份时发生错误")
            self.status_var.set("就绪")
        
        # 启动线程
        thread = threading.Thread(target=backup_thread)
        thread.daemon = True
        thread.start()
    
    def restore_backup(self):
        """
        恢复备份
        """
        # 获取选中的项
        selected_item = self.backup_tree.selection()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个备份")
            return
        
        # 获取版本ID
        version_id = self.backup_tree.item(selected_item[0])["values"][0]
        
        # 确认恢复
        confirm = messagebox.askyesno("恢复备份", 
                                    f"确定要恢复到版本 {version_id} 吗？\n" +
                                    "这将覆盖当前项目的所有文件！")
        if not confirm:
            return
        
        # 开始恢复线程
        def restore_thread():
            self.status_var.set(f"正在恢复到版本 {version_id}...")
            result = self.backup_tool.restore_backup(version_id)
            if result:
                messagebox.showinfo("恢复成功", f"已恢复到版本: {version_id}")
                self.load_backups()
            else:
                messagebox.showerror("恢复失败", "恢复备份时发生错误")
            self.status_var.set("就绪")
        
        # 启动线程
        thread = threading.Thread(target=restore_thread)
        thread.daemon = True
        thread.start()
    
    def delete_backup(self):
        """
        删除备份
        """
        # 获取选中的项
        selected_item = self.backup_tree.selection()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个备份")
            return
        
        # 获取版本ID
        version_id = self.backup_tree.item(selected_item[0])["values"][0]
        
        # 确认删除
        confirm = messagebox.askyesno("删除备份", 
                                    f"确定要删除版本 {version_id} 吗？\n" +
                                    "此操作不可恢复！")
        if not confirm:
            return
        
        # 开始删除线程
        def delete_thread():
            self.status_var.set(f"正在删除版本 {version_id}...")
            result = self.backup_tool.delete_backup(version_id)
            if result:
                messagebox.showinfo("删除成功", f"已删除版本: {version_id}")
                self.load_backups()
            else:
                messagebox.showerror("删除失败", "删除备份时发生错误")
            self.status_var.set("就绪")
        
        # 启动线程
        thread = threading.Thread(target=delete_thread)
        thread.daemon = True
        thread.start()
    
    def on_double_click(self, event):
        """
        双击事件处理（查看备份详情）
        """
        # 获取选中的项
        selected_item = self.backup_tree.selection()
        if not selected_item:
            return
        
        # 获取版本ID
        version_id = self.backup_tree.item(selected_item[0])["values"][0]
        
        # 查找备份信息
        backup = next((b for b in self.backup_tool.backup_log if b["id"] == version_id), None)
        if not backup:
            return
        
        # 显示详情
        details = f"版本ID: {backup['id']}\n"
        details += f"备份时间: {backup['timestamp']}\n"
        details += f"注释: {backup['comment']}\n"
        details += f"备份类型: {'压缩' if backup.get('compression', True) else '文件夹'}\n"
        details += f"备份路径: {backup['path']}\n"
        
        messagebox.showinfo("备份详情", details)
    

def main():
    """
    主函数
    """
    root = tk.Tk()
    
    # 设置样式
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="red")
    
    app = BackupToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()