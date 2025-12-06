import tkinter as tk
from tkinter import ttk, messagebox
import time
import math

class GraphColoringVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Coloring Backtracking Visualizer")
        self.root.geometry("1000x750")
        self.root.configure(bg="#000")
        
        self.V = 0
        self.edges = []
        self.m = 0
        self.delay = 0.8
        self.color = []
        self.adj = []
        self.colors_hex = ["#FF4444", "#44FF44", "#4444FF", "#FF44FF", "#FFFF44", 
                          "#FF44AA", "#44FFFF", "#FFA500", "#800080", "#00FF00"]
        self.positions = []
        self.solving = False
        self.setup_mode = True
        
        self.create_frontend()
        
    def create_frontend(self):
        # Main title
        title = tk.Label(self.root, text="Graph Coloring Backtracking Visualizer", 
                        font=("Consolas", 20, "bold"), fg="#0f0", bg="#000")
        title.pack(pady=15)
        
        # Configuration frame
        config_frame = tk.Frame(self.root, bg="#000")
        config_frame.pack(pady=10)
        
        # Number of vertices
        tk.Label(config_frame, text="Number of Vertices:", font=("Consolas", 12),
                fg="#0ff", bg="#000").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.vertices_var = tk.StringVar(value="5")
        vertices_entry = ttk.Entry(config_frame, textvariable=self.vertices_var, 
                                   width=10, font=("Consolas", 11))
        vertices_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Number of colors
        tk.Label(config_frame, text="Number of Colors:", font=("Consolas", 12),
                fg="#0ff", bg="#000").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.colors_var = tk.StringVar(value="3")
        colors_entry = ttk.Entry(config_frame, textvariable=self.colors_var, 
                                width=10, font=("Consolas", 11))
        colors_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Speed control
        tk.Label(config_frame, text="Animation Speed:", font=("Consolas", 12),
                fg="#0ff", bg="#000").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.speed_var = tk.DoubleVar(value=0.8)
        speed_scale = ttk.Scale(config_frame, from_=0.1, to=2.0, variable=self.speed_var,
                               orient=tk.HORIZONTAL, length=150)
        speed_scale.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(config_frame, text="(Fast → Slow)", font=("Consolas", 9),
                fg="#888", bg="#000").grid(row=2, column=2, padx=5, pady=5)
        
        # Graph type selection
        tk.Label(config_frame, text="Graph Type:", font=("Consolas", 12),
                fg="#0ff", bg="#000").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.graph_type = tk.StringVar(value="cycle")
        graph_dropdown = ttk.Combobox(config_frame, textvariable=self.graph_type,
                                     values=["cycle", "complete", "star", "custom"],
                                     state="readonly", width=12, font=("Consolas", 10))
        graph_dropdown.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#000")
        btn_frame.pack(pady=15)
        
        self.generate_btn = tk.Button(btn_frame, text="Generate Graph", 
                                      command=self.generate_graph,
                                      font=("Consolas", 12, "bold"), 
                                      bg="#0a0", fg="white", padx=20, pady=8)
        self.generate_btn.grid(row=0, column=0, padx=10)
        
        self.start_btn = tk.Button(btn_frame, text="Start Coloring", 
                                   command=self.start_coloring,
                                   font=("Consolas", 12, "bold"), 
                                   bg="#00a", fg="white", padx=20, pady=8,
                                   state=tk.DISABLED)
        self.start_btn.grid(row=0, column=1, padx=10)
        
        self.reset_btn = tk.Button(btn_frame, text="Reset", 
                                   command=self.reset_graph,
                                   font=("Consolas", 12, "bold"), 
                                   bg="#a00", fg="white", padx=20, pady=8,
                                   state=tk.DISABLED)
        self.reset_btn.grid(row=0, column=2, padx=10)
        
        # Status label
        self.status = tk.Label(self.root, text="Configure and generate your graph to begin!", 
                              font=("Consolas", 13), fg="yellow", bg="#000")
        self.status.pack(pady=10)
        
        # Canvas
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="#111", 
                               highlightthickness=2, highlightbackground="#0f0")
        self.canvas.pack(pady=10)
        
        # Instructions for custom graph
        self.instructions = tk.Label(self.root, 
                                     text="For custom graphs: Click on two vertices to add an edge",
                                     font=("Consolas", 10), fg="#888", bg="#000")
        
        self.canvas.bind("<Button-1>", self.canvas_click)
        
    def generate_graph(self):
        try:
            self.V = int(self.vertices_var.get())
            self.m = int(self.colors_var.get())
            self.delay = float(self.speed_var.get())
            
            if self.V < 2 or self.V > 20:
                messagebox.showerror("Error", "Number of vertices must be between 2 and 20")
                return
            if self.m < 1 or self.m > 10:
                messagebox.showerror("Error", "Number of colors must be between 1 and 10")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return
        
        # Generate edges based on graph type
        graph_type = self.graph_type.get()
        self.edges = []
        
        if graph_type == "cycle":
            # Cycle graph: vertices connected in a ring
            for i in range(self.V):
                self.edges.append([i, (i + 1) % self.V])
                
        elif graph_type == "complete":
            # Complete graph: all vertices connected
            for i in range(self.V):
                for j in range(i + 1, self.V):
                    self.edges.append([i, j])
                    
        elif graph_type == "star":
            # Star graph: one center connected to all others
            for i in range(1, self.V):
                self.edges.append([0, i])
                
        elif graph_type == "custom":
            # Custom graph: user will click to add edges
            self.instructions.pack(pady=5)
            self.selected_vertex = None
        
        # Initialize graph structures
        self.color = [-1] * self.V
        self.adj = [[] for _ in range(self.V)]
        
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # Calculate vertex positions
        self.positions = []
        radius = 200
        cx, cy = 350, 250
        for i in range(self.V):
            angle = 2 * math.pi * i / self.V - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            self.positions.append((x, y))
        
        # Draw graph
        self.draw_graph()
        
        # Enable buttons
        if graph_type != "custom" or len(self.edges) > 0:
            self.start_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        
        self.status.config(text=f"Graph generated: {self.V} vertices, {len(self.edges)} edges. Ready!", 
                          fg="#0f0")
        
    def canvas_click(self, event):
        if self.graph_type.get() != "custom" or self.V == 0:
            return
            
        # Find clicked vertex
        clicked_vertex = None
        for i in range(self.V):
            x, y = self.positions[i]
            dist = math.sqrt((event.x - x)**2 + (event.y - y)**2)
            if dist <= 45:
                clicked_vertex = i
                break
        
        if clicked_vertex is None:
            return
        
        if self.selected_vertex is None:
            self.selected_vertex = clicked_vertex
            self.highlight_vertex(clicked_vertex)
        else:
            if self.selected_vertex != clicked_vertex:
                # Add edge
                edge = sorted([self.selected_vertex, clicked_vertex])
                if edge not in [sorted(e) for e in self.edges]:
                    self.edges.append(edge)
                    self.adj[edge[0]].append(edge[1])
                    self.adj[edge[1]].append(edge[0])
                    self.draw_graph()
                    self.status.config(text=f"Edge added: {edge[0]} ↔ {edge[1]}", fg="#0f0")
                    if len(self.edges) > 0:
                        self.start_btn.config(state=tk.NORMAL)
            self.selected_vertex = None
    
    def highlight_vertex(self, v):
        x, y = self.positions[v]
        self.canvas.create_oval(x-50, y-50, x+50, y+50, outline="yellow", width=3, tags="highlight")
        self.root.after(300, lambda: self.canvas.delete("highlight"))
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Draw edges
        for u, v in self.edges:
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="#666", width=4)
        
        # Draw vertices
        for i in range(self.V):
            x, y = self.positions[i]
            fill = self.colors_hex[self.color[i]] if self.color[i] != -1 else "#333"
            self.canvas.create_oval(x-45, y-45, x+45, y+45, fill=fill, 
                                   outline="#0f0", width=4)
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 24, "bold"), 
                                   fill="white")
    
    def issafe(self, v, c):
        for nei in self.adj[v]:
            if self.color[nei] == c:
                return False
        return True
    
    def solve_step(self, v):
        if v == self.V:
            self.status.config(text="SUCCESS! Valid coloring found! ✓", fg="#0f0")
            self.solving = False
            return True
        
        self.status.config(text=f"Trying vertex {v}...", fg="cyan")
        self.root.update()
        time.sleep(self.delay * 0.7)
        
        for c in range(self.m):
            if self.issafe(v, c):
                self.color[v] = c
                self.status.config(text=f"Vertex {v} → Color {c}", fg="#0f0")
                self.draw_graph()
                self.root.update()
                time.sleep(self.delay)
                
                if self.solve_step(v + 1):
                    return True
                
                # Backtrack
                self.status.config(text=f"Backtracking vertex {v}...", fg="#f44")
                self.color[v] = -1
                self.draw_graph()
                self.root.update()
                time.sleep(self.delay * 0.8)
        
        self.status.config(text=f"No valid color for vertex {v}", fg="orange")
        return False
    
    def start_coloring(self):
        if self.solving:
            return
        
        self.solving = True
        self.generate_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        
        # Reset colors
        self.color = [-1] * self.V
        self.draw_graph()
        
        self.status.config(text="Starting backtracking algorithm...", fg="white")
        self.root.after(100, self.run_solver)
    
    def run_solver(self):
        success = self.solve_step(0)
        if not success:
            self.status.config(text=f"FAILED: Cannot color with {self.m} colors! ✗", 
                             fg="red")
        
        self.solving = False
        self.generate_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)
    
    def reset_graph(self):
        self.color = [-1] * self.V
        self.draw_graph()
        self.status.config(text="Graph reset. Ready to color again!", fg="gray")
        self.start_btn.config(state=tk.NORMAL)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GraphColoringVisualizer()
    app.run()