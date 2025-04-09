
class A():
    def __init__(self):
        self.name:list[str] = []


    def volume(self, height: float, area: float) -> float:
        if height < 0 or area < 0:
            raise ValueError("Height and area must be non-negative")
        return height * area
    


class B(A):
    def __init__(self):
        super().__init__()

    def get_volume(self,height:int, area:float) -> str:
        vol : float = self.volume(height,area)
        return f"{vol:.2f} is the volume"        
    


if __name__ == "__main__": # pragma: no cover
    b : B = B()
    print(b.get_volume(11,45.55))