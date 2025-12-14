import json
import os

# 文本文件路径
new_obj_file = "new_outbound.json"

# 从文本文件读取新对象数组
with open(new_obj_file, "r", encoding="utf-8") as f:
    new_objs = json.load(f)

if not isinstance(new_objs, list):
    raise ValueError("new_outbound.json 必须包含一个数组")

# 遍历当前目录下所有 JSON 文件
for filename in os.listdir("."):
    if filename.endswith("_config.json"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 找到 tag 为 "proxy-out" 的对象
        for outbound in data.get("outbounds", []):
            if outbound.get("tag") == "proxy-out":
                for new_obj in new_objs:
                    new_tag = new_obj.get("tag")
                    if not new_tag:
                        raise ValueError("新对象必须包含 'tag' 属性")

                    # 添加新对象的 tag 到 proxy-out 的 outbounds
                    outbound_outbounds = outbound.get("outbounds", [])
                    if new_tag not in outbound_outbounds:
                        outbound_outbounds.append(new_tag)
                    outbound["outbounds"] = outbound_outbounds

                    # 修改 default 为新对象的 tag
                    outbound["default"] = new_tag

        # 将新对象数组添加到根级 outbounds 中
        for new_obj in new_objs:
            data["outbounds"].append(new_obj)

        # 保存修改后的 JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"{filename} 已更新。")
