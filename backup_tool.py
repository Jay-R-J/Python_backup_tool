#!/usr/bin/env python3
"""
项目自动备份工具
作者：Jay
版本：1.0
"""

import os
import shutil
import json
import datetime
import sys
import hashlib
from pathlib import Path
import zipfile
import argparse
from typing import List, Dict, Optional


class ProjectBackupTool:

    def __init__(self, config_file: str = "config.json"):
        """
        初始化备份工具
        """
        self.current_dir = Path.cwd()
        self.config_file = self.current_dir / config_file
        self.config = self.load_config()
        
        # 设置源目录（要备份的目录）
        self.source_dir = Path(self.config.get("source_dir", self.current_dir))
        
        # 设置备份目录（直接保存备份文件的目录，不自动创建子目录）
        self.backup_dir = Path(self.config.get("backup_dir", 
                              self.current_dir.parent / "project_backups"))
        
        # 确保备份目录存在
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 备份日志文件
        self.log_file = self.backup_dir / "backup_log.json"
        self.backup_log = self.load_backup_log()
    
    def set_source_dir(self, source_dir: str):
        """
        设置要备份的源目录
        """
        self.source_dir = Path(source_dir)
        # 更新项目名称为源目录名称
        self.project_name = self.source_dir.name
        # 备份日志文件仍保存在当前备份目录
        self.log_file = self.backup_dir / "backup_log.json"
        self.backup_log = self.load_backup_log()
        
        # 更新配置
        self.config["source_dir"] = source_dir
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
        print(f"✓ 已更新源目录: {self.source_dir}")
    
    def set_backup_dir(self, backup_dir: str):
        """
        设置备份文件保存目录
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.backup_dir / "backup_log.json"
        self.backup_log = self.load_backup_log()
        
        # 更新配置
        self.config["backup_dir"] = backup_dir
        # 删除旧的配置项（如果存在）
        if "backup_root" in self.config:
            del self.config["backup_root"]
        if "project_backup_dir" in self.config:
            del self.config["project_backup_dir"]
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
        print(f"✓ 已更新备份目录: {self.backup_dir}")
    
    def load_config(self) -> Dict:
        """
        加载配置文件
        """
        default_config = {
            "backup_root": str(self.current_dir.parent / "project_backups"),
            "auto_exclude": [
                ".git", "node_modules", "__pycache__", ".pytest_cache",
                "venv", ".venv", "env", ".env", ".idea", ".vscode",
                ".DS_Store", "*.pyc", "*.log", "*.tmp", "*.bak",
                "backup_*", "dist", "build", "*.egg-info"
            ],
            "max_backups": 50,
            "compression": True,
            "hash_check": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 合并配置（用户配置覆盖默认配置）
                default_config.update(user_config)
                print(f"✓ 已加载配置文件: {self.config_file}")
            except json.JSONDecodeError:
                print(f"⚠ 配置文件格式错误，使用默认配置")
        else:
            # 创建默认配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            print(f"✓ 已创建默认配置文件: {self.config_file}")
        
        return default_config
    
    def load_backup_log(self) -> List[Dict]:
        """
        加载备份日志
        """
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_backup_log(self):
        """
        保存备份日志
        """
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.backup_log, f, indent=4, ensure_ascii=False)
    
    def calculate_file_hash(self, filepath: Path) -> str:
        """
        计算文件哈希值（用于校验）
        """
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return ""
    
    def should_exclude(self, path: Path) -> bool:
        """
        判断是否应该排除该文件/文件夹
        """
        path_str = str(path)
        
        # 排除备份目录本身
        if self.backup_dir in path.parents:
            return True
        
        # 排除配置文件（仅当配置文件在工具运行目录时）
        if path.name == "config.json" and path.parent == self.current_dir:
            return True
        
        # 排除自身脚本（仅当脚本在工具运行目录时）
        if path.name == "backup_tool.py" and path.parent == self.current_dir:
            return True
        
        if path.name == "gui_backup_tool.py" and path.parent == self.current_dir:
            return True
        
        # 检查排除规则
        for pattern in self.config["auto_exclude"]:
            if pattern.startswith("*"):
                # 文件扩展名匹配
                if path_str.endswith(pattern[1:]):
                    return True
            elif path.name == pattern:
                return True
            elif pattern in path_str:
                return True
        
        return False
    
    def create_zip_backup(self, backup_path: Path, version_id: str):
        """
        创建压缩备份（支持大文件）
        """
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                # 过滤掉需要排除的目录
                dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d)]
                
                for file in files:
                    file_path = Path(root) / file
                    if not self.should_exclude(file_path):
                        # 计算相对路径
                        rel_path = file_path.relative_to(self.source_dir)
                        zipf.write(file_path, rel_path)
    
    def create_folder_backup(self, backup_path: Path, version_id: str):
        """
        创建文件夹备份（支持大文件）
        """
        for root, dirs, files in os.walk(self.source_dir):
            # 过滤掉需要排除的目录
            dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                if not self.should_exclude(file_path):
                    # 计算相对路径
                    rel_path = file_path.relative_to(self.source_dir)
                    dest_path = backup_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
    
    def create_backup(self, comment: str = ""):
        """
        创建项目备份
        """
        try:
            # 生成时间戳和版本号
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            version_id = f"v{len(self.backup_log) + 1:03d}_{timestamp_str}"
            
            # 使用源目录名称作为项目名称
            self.project_name = self.source_dir.name
            
            # 创建备份文件名称
            backup_name = f"{self.project_name}_{version_id}"
            if comment:
                backup_name += f"_{comment.replace(' ', '_')}"
            
            # 直接保存到用户选择的备份目录
            backup_path = self.backup_dir / backup_name
            
            # 如果是压缩模式
            if self.config.get("compression", True):
                backup_path = backup_path.with_suffix('.zip')
                self.create_zip_backup(backup_path, version_id)
            else:
                backup_path.mkdir(parents=True, exist_ok=True)
                self.create_folder_backup(backup_path, version_id)
            
            # 记录备份信息
            backup_info = {
                "id": version_id,
                "name": backup_name,
                "timestamp": timestamp.isoformat(),
                "path": str(backup_path),
                "comment": comment,
                "compression": self.config.get("compression", True)
            }
            
            self.backup_log.append(backup_info)
            self.save_backup_log()
            
            print(f"✓ 备份成功: {backup_path}")
            return backup_info
        except Exception as e:
            print(f"✗ 备份失败: {e}")
            return None
    
    def list_backups(self) -> List[Dict]:
        """
        列出所有备份（只返回实际存在的备份）
        """
        # 过滤掉不存在的备份文件
        existing_backups = []
        for backup in self.backup_log:
            if Path(backup["path"]).exists():
                existing_backups.append(backup)
            else:
                # 如果备份文件不存在，从日志中移除
                self.backup_log = [b for b in self.backup_log if b["id"] != backup["id"]]
                self.save_backup_log()
        
        return sorted(existing_backups, key=lambda x: x["timestamp"], reverse=True)
    
    def restore_backup(self, version_id: str):
        """
        恢复到指定版本
        """
        # 查找指定版本
        backup_info = next((b for b in self.backup_log if b["id"] == version_id), None)
        if not backup_info:
            print(f"✗ 未找到版本: {version_id}")
            return False
        
        backup_path = Path(backup_info["path"])
        if not backup_path.exists():
            print(f"✗ 备份文件不存在: {backup_path}")
            return False
        
        try:
            # 清空源目录，跳过无法删除的文件
            failed_to_delete = []
            for item in self.source_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
                except PermissionError:
                    failed_to_delete.append(str(item))
                except Exception as e:
                    failed_to_delete.append(f"{item} ({str(e)})")
            
            # 恢复备份，跳过无法写入的文件
            failed_to_restore = []
            
            if backup_path.suffix == '.zip':
                # 从压缩文件恢复
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    for file_info in zipf.infolist():
                        try:
                            zipf.extract(file_info, self.source_dir)
                        except PermissionError:
                            failed_to_restore.append(file_info.filename)
                        except Exception as e:
                            failed_to_restore.append(f"{file_info.filename} ({str(e)})")
            else:
                # 从文件夹恢复
                for root, dirs, files in os.walk(backup_path):
                    rel_path = Path(root).relative_to(backup_path)
                    for file in files:
                        src_file = Path(root) / file
                        dest_file = self.source_dir / rel_path / file
                        try:
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src_file, dest_file)
                        except PermissionError:
                            failed_to_restore.append(str(rel_path / file))
                        except Exception as e:
                            failed_to_restore.append(f"{rel_path / file} ({str(e)})")
            
            # 输出恢复结果
            print(f"✓ 已恢复到版本: {version_id}")
            
            # 输出无法删除的文件信息
            if failed_to_delete:
                print(f"⚠ 以下 {len(failed_to_delete)} 个文件/目录无法删除（权限问题）:")
                for item in failed_to_delete[:10]:  # 只显示前10个
                    print(f"  - {item}")
                if len(failed_to_delete) > 10:
                    print(f"  ... 以及 {len(failed_to_delete) - 10} 个其他项目")
            
            # 输出无法恢复的文件信息
            if failed_to_restore:
                print(f"⚠ 以下 {len(failed_to_restore)} 个文件无法恢复（权限问题）:")
                for item in failed_to_restore[:10]:  # 只显示前10个
                    print(f"  - {item}")
                if len(failed_to_restore) > 10:
                    print(f"  ... 以及 {len(failed_to_restore) - 10} 个其他文件")
            
            return True
        except Exception as e:
            print(f"✗ 恢复失败: {e}")
            return False
    
    def delete_backup(self, version_id: str):
        """
        删除指定备份
        """
        # 查找指定版本
        backup_info = next((b for b in self.backup_log if b["id"] == version_id), None)
        if not backup_info:
            print(f"✗ 未找到版本: {version_id}")
            return False
        
        backup_path = Path(backup_info["path"])
        if not backup_path.exists():
            print(f"✗ 备份文件不存在: {backup_path}")
            return False
        
        try:
            if backup_path.is_dir():
                shutil.rmtree(backup_path)
            else:
                backup_path.unlink()
            
            # 从日志中移除
            self.backup_log = [b for b in self.backup_log if b["id"] != version_id]
            self.save_backup_log()
            
            print(f"✓ 已删除版本: {version_id}")
            return True
        except Exception as e:
            print(f"✗ 删除失败: {e}")
            return False
    
    def clean_old_backups(self):
        """
        清理旧备份，保留最新的N个
        """
        max_backups = self.config.get("max_backups", 50)
        if len(self.backup_log) <= max_backups:
            return
        
        # 按时间排序，保留最新的max_backups个
        sorted_backups = sorted(self.backup_log, key=lambda x: x["timestamp"])
        backups_to_delete = sorted_backups[:-max_backups]
        
        for backup_info in backups_to_delete:
            self.delete_backup(backup_info["id"])


def main():
    """
    命令行入口
    """
    parser = argparse.ArgumentParser(description="项目自动备份工具")
    parser.add_argument("-c", "--create", action="store_true", help="创建备份")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有备份")
    parser.add_argument("-r", "--restore", type=str, help="恢复到指定版本")
    parser.add_argument("-d", "--delete", type=str, help="删除指定版本")
    parser.add_argument("-C", "--comment", type=str, default="", help="备份时添加注释")
    args = parser.parse_args()
    
    backup_tool = ProjectBackupTool()
    
    if args.create:
        backup_tool.create_backup(args.comment)
    elif args.list:
        backups = backup_tool.list_backups()
        for backup in backups:
            print(f"{backup['id']} - {backup['timestamp']} - {backup['comment']}")
    elif args.restore:
        backup_tool.restore_backup(args.restore)
    elif args.delete:
        backup_tool.delete_backup(args.delete)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()