import threading,random,time

class Vehiculo(threading.Thread):
    def __init__(self,id,canvas,y,meta,rondas,control,callback,img):
        super().__init__()
        self.id=id
        self.canvas=canvas
        self.y=y
        self.meta=meta
        self.rondas=rondas
        self.control=control
        self.callback=callback
        self.x=30
        self.tiempo=0
        self.img=img
        self.obj=self.canvas.create_image(self.x,self.y,image=self.img,anchor="w")
        self.txt=self.canvas.create_text(self.x+20,self.y+10,text=str(self.id),fill="white")

    def mover(self,dx):
        self.canvas.after(0,self.canvas.move,self.obj,dx,0)
        self.canvas.after(0,self.canvas.move,self.txt,dx,0)

    def run(self):
        inicio=time.perf_counter()
        while self.x<self.meta:
            velocidad=random.uniform(2,7)
            factor=self.control
            dx=velocidad
            self.x+=dx
            if self.x>self.meta:
                dx-=self.x-self.meta
                self.x=self.meta
            self.mover(dx)
            time.sleep(0.02*factor)
        self.tiempo=time.perf_counter()-inicio
        self.callback(self)