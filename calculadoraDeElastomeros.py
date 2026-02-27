import customtkinter as ctk
import math
from tkinter import messagebox

ctk.set_appearance_mode("dark")

class HutchinsonTooling(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Elastômeros")
        self.geometry("1200x850")
        
        self.materiais = {
            "EPDM (Automotivo)": {"contr": 2.5, "swell": 1.25},
            "NBR (Nitrílica)": {"contr": 1.8, "swell": 1.15},
            "SBR": {"contr": 2.0, "swell": 1.20},
            "Viton (FKM)": {"contr": 3.0, "swell": 1.08}
        }

        self.layout_config()
        self.init_widgets()

    def layout_config(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def init_widgets(self):
        self.sidebar = ctk.CTkScrollableFrame(self, width=400)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="Calculadora de Elastômeros", font=("Segoe UI", 24, "bold")).pack(pady=20)

        self.combo_mat = ctk.CTkComboBox(self.sidebar, values=list(self.materiais.keys()), width=300)
        self.combo_mat.set("EPDM (Automotivo)")
        self.combo_mat.pack(pady=10)

        self.in_nominal = self.add_field("Medida Nominal (mm)", "25.0")
        self.in_area = self.add_field("Área Projetada (cm²)", "180")
        self.in_espessura = self.add_field("Espessura Parede (mm)", "4.0")
        self.in_pressao = self.add_field("Pressão Vulcanização (Bar)", "150")
        self.in_fio = self.add_field("Offset Fio (mm)", "0.15")
        self.in_fresa = self.add_field("Ø Fresa (mm)", "10.0")

        self.btn_run = ctk.CTkButton(self.sidebar, text="CALCULAR", command=self.process_data, 
                                    height=50, fg_color="#d35400", hover_color="#a04000")
        self.btn_run.pack(pady=30)

        self.log_area = ctk.CTkTextbox(self, font=("Consolas", 14))
        self.log_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def add_field(self, label, val):
        ctk.CTkLabel(self.sidebar, text=label).pack(anchor="w", padx=50)
        entry = ctk.CTkEntry(self.sidebar, width=300)
        entry.insert(0, val)
        entry.pack(pady=5)
        return entry

    def process_data(self):
        try:
            m = self.materiais[self.combo_mat.get()]
            nom = float(self.in_nominal.get())
            area = float(self.in_area.get())
            pres = float(self.in_pressao.get())
            
            # Lógica de Cálculo
            d_matriz = nom / m["swell"]
            ton = (area * (pres/10)) / 10
            cura = (float(self.in_espessura.get()) / 1.5) * 60

            self.log_area.delete("1.0", "end")
            res =  f"--- RELATÓRIO TÉCNICO HBA ---\n\n"
            res += f"Matriz CAD: {d_matriz:.3f} mm (Swell: {m['swell']})\n"
            res += f"Fechamento: {ton:.2f} Ton\n"
            res += f"Tempo Cura: {cura:.1f} s\n"
            res += f"Escala Molde: {1 + (m['contr']/100):.4f}\n"
            res += f"Raio Mín. Canto: {(float(self.in_fresa.get())/2)+0.2:.2f} mm"
            
            self.log_area.insert("0.0", res)
        except:
            messagebox.showerror("Erro", "Valores inválidos.")

if __name__ == "__main__":
    app = HutchinsonTooling()
    app.mainloop()
