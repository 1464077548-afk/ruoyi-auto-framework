    def _handle_role_placeholder(self, selector, description):
        """处理 role+placeholder 组合定位"""
        role = selector["role"]
        placeholder = selector["placeholder"]
        if "*" in placeholder:
            placeholder = re.compile(re.escape(placeholder).replace(r"\*", ".*"))
        
        # 提取除了 role 和 placeholder 之外的其他参数
        role_kwargs = {k: v for k, v in selector.items() if k != "role" and k != "placeholder"}
        
        print(f"使用{description}定位元素，role={role}, placeholder={selector['placeholder']}, 其他参数={role_kwargs}")
        # 先通过 role 定位，支持其他参数如 name
        role_locator = self.page.get_by_role(role, **role_kwargs)
        # 再在 role 定位的基础上通过 placeholder 定位
        return role_locator.get_by_placeholder(placeholder)
