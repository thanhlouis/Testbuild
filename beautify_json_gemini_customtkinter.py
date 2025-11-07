import customtkinter as ctk
import json
import time

# Cài đặt giao diện cơ bản
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JsonConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Cấu hình cửa sổ ---
        self.title("JSON/Netscape Converter Tool (Customtkinter)")
        self.geometry("980x1020")

        # --- Tạo Layout ---
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 3, 4), weight=1) 
        self.grid_rowconfigure((2, 5), weight=0)

        # --- Khởi tạo Widgets ---
        self._setup_widgets()

    def _setup_widgets(self):
        # 1. Netscape Input (Convert to JSON)
        self.netscape_frame = ctk.CTkFrame(self)
        self.netscape_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.netscape_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.netscape_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.netscape_frame, text="Netscape Cookie Input (Convert to JSON Type 1 & 2):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.netscape_frame, text="Paste", width=80, command=lambda: self.paste_from_clipboard(self.netscape_input, self.on_netscape_input_changed)).grid(row=0, column=2, padx=10, pady=(10, 0), sticky="e")
        self.netscape_input = ctk.CTkTextbox(self.netscape_frame, height=120)
        self.netscape_input.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.netscape_input.bind("<KeyRelease>", self.on_netscape_input_changed)
        
        # 2. JSON Input (Beautify/Compact)
        self.beautify_frame = ctk.CTkFrame(self)
        self.beautify_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.beautify_frame.grid_columnconfigure((0, 1), weight=1)
        self.beautify_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.beautify_frame, text="JSON Input (Beautify/Compact/Filter):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.beautify_frame, text="Paste", width=80, command=lambda: self.paste_from_clipboard(self.json_beautify_input, self.beautify_and_compact_json)).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.json_beautify_input = ctk.CTkTextbox(self.beautify_frame, height=120)
        self.json_beautify_input.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.json_beautify_input.bind("<KeyRelease>", self.beautify_and_compact_json)

        # 3. JSON Input (Convert to Netscape)
        self.netscape_convert_frame = ctk.CTkFrame(self)
        self.netscape_convert_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.netscape_convert_frame.grid_columnconfigure((0, 1), weight=1)
        self.netscape_convert_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.netscape_convert_frame, text="JSON Input (Convert to Netscape Cookie Format):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.netscape_convert_frame, text="Paste", width=80, command=lambda: self.paste_from_clipboard(self.json_to_netscape_input, self.on_json_to_netscape_changed)).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.json_to_netscape_input = ctk.CTkTextbox(self.netscape_convert_frame, height=120)
        self.json_to_netscape_input.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.json_to_netscape_input.bind("<KeyRelease>", self.on_json_to_netscape_changed)

        # 4. Cookie Filter Controls
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.filter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.filter_frame, text="Cookie Filter (Tên cách nhau bằng dấu phẩy ','):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.cookie_names_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="Tên cookie 1, Tên cookie 2, ...")
        self.cookie_names_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.cookie_names_entry.bind("<KeyRelease>", self.update_filter_status)
        
        self.filter_checkbox = ctk.CTkCheckBox(self.filter_frame, text="Chỉ lấy Cookie theo danh sách tên đã nhập", command=self.update_filter_status)
        self.filter_checkbox.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        # 5. Result (JSON Type 1 - Beautify)
        self.result_type1_frame = ctk.CTkFrame(self)
        self.result_type1_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.result_type1_frame.grid_columnconfigure((0, 1), weight=1)
        self.result_type1_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.result_type1_frame, text="Result (JSON Type 1 - Object with 'url' and 'cookies' / Beautify):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.result_type1_frame, text="Copy", width=80, command=lambda: self.copy_to_clipboard(self.json_output_type1)).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.json_output_type1 = ctk.CTkTextbox(self.result_type1_frame)
        self.json_output_type1.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 6. Result (JSON Type 2 - Array / Compact)
        self.result_type2_frame = ctk.CTkFrame(self)
        self.result_type2_frame.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
        self.result_type2_frame.grid_columnconfigure((0, 1), weight=1)
        self.result_type2_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.result_type2_frame, text="Result (JSON Type 2 - Cookie Array / Compact JSON):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.result_type2_frame, text="Copy", width=80, command=lambda: self.copy_to_clipboard(self.json_output_type2)).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.json_output_type2 = ctk.CTkTextbox(self.result_type2_frame)
        self.json_output_type2.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 7. Result (Netscape Format)
        self.result_netscape_frame = ctk.CTkFrame(self)
        self.result_netscape_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.result_netscape_frame.grid_columnconfigure((0, 1), weight=1)
        self.result_netscape_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.result_netscape_frame, text="Result (Netscape Cookie Format):").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkButton(self.result_netscape_frame, text="Copy", width=80, command=lambda: self.copy_to_clipboard(self.netscape_output)).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.netscape_output = ctk.CTkTextbox(self.result_netscape_frame, height=120)
        self.netscape_output.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 8. Time Label
        self.time_label = ctk.CTkLabel(self, text="Processing Time: ")
        self.time_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        self.json_output_type1.configure(state="disabled")
        self.json_output_type2.configure(state="disabled")
        self.netscape_output.configure(state="disabled")

    # --- HANDLERS ---
    
    def paste_from_clipboard(self, box, callback):
        try:
            text = self.clipboard_get()
            if text:
                box.delete("1.0", "end")
                box.insert("1.0", text)
                callback() 
        except Exception:
            pass 
            
    def get_filter_list(self):
        if not self.filter_checkbox.get():
            return None 
        
        names_text = self.cookie_names_entry.get().strip()
        if not names_text:
            return set() 
        
        names = [name.strip().lower() for name in names_text.split(',') if name.strip()]
        return set(names)
        
    def update_filter_status(self, event=None):
        """Kích hoạt lại các chuyển đổi khi thay đổi cài đặt filter"""
        # Cập nhật cho Netscape Input
        netscape_data = self.netscape_input.get("1.0", "end-1c")
        if netscape_data.strip():
            self.convert_to_json_cookie(netscape_data)
        
        # Cập nhật cho JSON (Beautify) Input
        beautify_data = self.json_beautify_input.get("1.0", "end-1c")
        if beautify_data.strip():
            self.beautify_and_compact_json() # Gọi lại hàm xử lý của nó
            
        # Cập nhật cho JSON (to Netscape) Input
        json_to_netscape_data = self.json_to_netscape_input.get("1.0", "end-1c")
        if json_to_netscape_data.strip():
            self.convert_json_to_netscape(json_to_netscape_data)

    def on_netscape_input_changed(self, event=None):
        input_data = self.netscape_input.get("1.0", "end-1c")
        self.clear_output_box(self.netscape_output) 
        self.convert_to_json_cookie(input_data)

    def beautify_and_compact_json(self, event=None):
        input_data = self.json_beautify_input.get("1.0", "end-1c")
        self.clear_output_box(self.netscape_output) 
        self.process_generic_json(input_data) # Sửa Lỗi 2: Gọi hàm đã được đại tu
        
    def on_json_to_netscape_changed(self, event=None):
        input_data = self.json_to_netscape_input.get("1.0", "end-1c")
        self.clear_output_boxes([self.json_output_type1, self.json_output_type2])
        self.convert_json_to_netscape(input_data)

    def set_output_box(self, box, text):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")
        
    def clear_output_box(self, box):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.configure(state="disabled")

    def clear_output_boxes(self, boxes):
        for box in boxes:
            self.clear_output_box(box)

    def copy_to_clipboard(self, box):
        box.configure(state="normal")
        # SỬA LỖI 1: Thay "1.M0" bằng "1.0"
        text_to_copy = box.get("1.0", "end-1c")
        box.configure(state="disabled")
        
        if text_to_copy:
            self.clipboard_clear()
            self.clipboard_append(text_to_copy)

    # --- CORE LOGIC ---

    def process_generic_json(self, input_data):
        """
        SỬA LỖI 2: Hàm này được viết lại hoàn toàn.
        Nó sẽ kiểm tra xem JSON có phải là cookie không.
        - Nếu CÓ: Lọc (Filter) rồi xuất ra Type 1 (Beautify) và Type 2 (Compact).
        - Nếu KHÔNG: Chỉ Beautify (Type 1) và Compact (Type 2) JSON gốc.
        """
        start_time = time.time()

        if not input_data.strip():
            self.clear_output_boxes([self.json_output_type1, self.json_output_type2, self.netscape_output])
            self.time_label.configure(text=f"Processing Time: 0 ms")
            return

        try:
            parsed_data = json.loads(input_data)
            cookies = []
            is_cookie_json = False

            # Cố gắng phát hiện định dạng cookie
            if isinstance(parsed_data, list):
                cookies = parsed_data
                # Kiểm tra heuristic: nếu là list, phần tử đầu tiên phải là dict có 'name'
                if not cookies or (isinstance(cookies[0], dict) and 'name' in cookies[0]):
                    is_cookie_json = True
            elif isinstance(parsed_data, dict) and 'cookies' in parsed_data and isinstance(parsed_data['cookies'], list):
                cookies = parsed_data['cookies']
                # Kiểm tra heuristic tương tự
                if not cookies or (isinstance(cookies[0], dict) and 'name' in cookies[0]):
                    is_cookie_json = True

            if is_cookie_json:
                # --- ĐÂY LÀ COOKIE JSON -> ÁP DỤNG LỌC ---
                filter_names = self.get_filter_list()
                filtered_cookies = []

                if filter_names is not None: # Lọc đang BẬT
                    for cookie in cookies:
                        name = cookie.get("name", "")
                        if name.lower() in filter_names:
                            filtered_cookies.append(cookie)
                else: # Lọc đang TẮT
                    filtered_cookies = cookies
                
                # 1. Ghi vào JSON Type 1 Result (Object, Beautify)
                default_domain = filtered_cookies[0]['domain'].lstrip('.') if filtered_cookies and filtered_cookies[0].get('domain') else "example.com"
                default_url = f"https://{default_domain}"
                json_data_type1_object = {
                    "url": default_url,
                    "cookies": filtered_cookies
                }
                beautified_json_type1 = json.dumps(json_data_type1_object, indent=4)
                self.set_output_box(self.json_output_type1, beautified_json_type1)
                
                # 2. Ghi vào JSON Type 2 Result (Array, Compact)
                # SỬA LỖI: Đổi từ compact (separators) sang beautify (indent=4) theo yêu cầu
                beautified_json_type2 = json.dumps(filtered_cookies, indent=4)
                self.set_output_box(self.json_output_type2, beautified_json_type2)
                
            else:
                # --- ĐÂY LÀ JSON THƯỜNG -> CHỈ LÀM ĐẸP/NÉN ---
                beautified_json = json.dumps(parsed_data, indent=4)
                self.set_output_box(self.json_output_type1, beautified_json)
                compact_json = json.dumps(parsed_data, separators=(',', ':'))
                self.set_output_box(self.json_output_type2, compact_json)

            self.clear_output_box(self.netscape_output) 

        except Exception as e:
            error_msg = f"Invalid JSON or processing error: {str(e)}"
            self.set_output_box(self.json_output_type1, error_msg)
            self.set_output_box(self.json_output_type2, error_msg)
            self.clear_output_box(self.netscape_output)
        
        elapsed_time = (time.time() - start_time) * 1000
        self.time_label.configure(text=f"Processing Time: {elapsed_time:.2f} ms (Beautify/Compact)")

    def convert_to_json_cookie(self, input_data):
        """
        Chuyển đổi Netscape sang JSON Loại 1 và Loại 2, có áp dụng lọc.
        """
        start_time = time.time()
        
        self.clear_output_boxes([self.json_output_type1, self.json_output_type2, self.netscape_output])

        lines = input_data.strip().splitlines()
        if not lines:
            elapsed_time = (time.time() - start_time) * 1000
            self.time_label.configure(text=f"Processing Time: {elapsed_time:.2f} ms")
            return
            
        filter_names = self.get_filter_list()
        
        cookies = []
        for line in lines:
            if line.strip().startswith('#'):
                continue
                
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            
            name = parts[5]
            
            if filter_names is not None:
                if name.lower() not in filter_names:
                    continue
            
            domain = parts[0]
            flag_http_only = parts[1].upper() == "TRUE" 
            path = parts[2]
            secure_flag_netscape = parts[3]
            expiration = parts[4] 
            value = parts[6]
            
            cookie = {
                "domain": domain,
                "expirationDate": int(float(expiration)) if expiration.replace('.', '', 1).isdigit() else 0,
                "httpOnly": flag_http_only,
                "name": name,
                "path": path,
                "secure": secure_flag_netscape.upper() == "TRUE",
                "value": value
            }
            cookies.append(cookie)

        # 1. Ghi vào JSON Type 1 Result (Object, Beautify)
        default_domain = cookies[0]['domain'].lstrip('.') if cookies and cookies[0].get('domain') else "example.com"
        default_url = f"https://{default_domain}"
        
        json_data_type1_object = {
            "url": default_url,
            "cookies": cookies
        }
        beautified_json_type1 = json.dumps(json_data_type1_object, indent=4)
        self.set_output_box(self.json_output_type1, beautified_json_type1)

        # 2. SỬA LỖI 3: Ghi vào JSON Type 2 Result (Array, Compact)
        # SỬA LỖI: Đổi từ compact (separators) sang beautify (indent=4) theo yêu cầu
        json_data_type2_array = cookies
        beautified_json_type2 = json.dumps(json_data_type2_array, indent=4) 
        self.set_output_box(self.json_output_type2, beautified_json_type2)
        
        elapsed_time = (time.time() - start_time) * 1000
        self.time_label.configure(text=f"Processing Time: {elapsed_time:.2f} ms (Netscape Conversion)")

    def convert_json_to_netscape(self, input_data):
        """Chuyển đổi JSON Loại 1 hoặc Loại 2 sang định dạng Netscape, có áp dụng lọc."""
        start_time = time.time()

        self.clear_output_boxes([self.json_output_type1, self.json_output_type2])

        if not input_data.strip():
            self.clear_output_box(self.netscape_output)
            elapsed_time = (time.time() - start_time) * 1000
            self.time_label.configure(text=f"Processing Time: {elapsed_time:.2f} ms")
            return

        try:
            parsed_data = json.loads(input_data)
            
            cookies = []
            if isinstance(parsed_data, list):
                cookies = parsed_data
            elif isinstance(parsed_data, dict) and 'cookies' in parsed_data and isinstance(parsed_data['cookies'], list):
                cookies = parsed_data['cookies']
            else:
                self.set_output_box(self.netscape_output, "Error: JSON is not a valid cookie format (Type 1 or Type 2).")
                return

            filter_names = self.get_filter_list()
            netscape_lines = []
            
            netscape_lines.append("# Netscape HTTP Cookie File")
            netscape_lines.append("# Generated by JsonConverterApp")
            netscape_lines.append("")
            
            for cookie in cookies:
                name = cookie.get("name", "")
                
                if filter_names is not None:
                    if name.lower() not in filter_names:
                        continue
                
                if not all(k in cookie for k in ["domain", "name", "value"]):
                    continue 

                domain = cookie.get("domain", "")
                http_only = cookie.get("httpOnly", False)
                flag = "TRUE" if http_only else "FALSE" 
                path = cookie.get("path", "/")
                secure = cookie.get("secure", False)
                secure_flag = "TRUE" if secure else "FALSE" 
                
                expiration_date = cookie.get("expirationDate")
                if expiration_date:
                    try:
                        expiration = str(int(float(expiration_date)))
                    except (ValueError, TypeError):
                        expiration = "0"
                else:
                    expiration = "0" 

                value = cookie.get("value", "")

                line = f"{domain}\t{flag}\t{path}\t{secure_flag}\t{expiration}\t{name}\t{value}"
                netscape_lines.append(line)

            netscape_output = "\n".join(netscape_lines)
            self.set_output_box(self.netscape_output, netscape_output)

        except json.JSONDecodeError as e:
            self.set_output_box(self.netscape_output, f"Error: Invalid JSON format.\n{str(e)}")
        except Exception as e:
            self.set_output_box(self.netscape_output, f"An unexpected error occurred: {str(e)}")
        
        elapsed_time = (time.time() - start_time) * 1000
        self.time_label.configure(text=f"Processing Time: {elapsed_time:.2f} ms (JSON -> Netscape Conversion)")


if __name__ == "__main__":
    app = JsonConverterApp()
    app.mainloop()
