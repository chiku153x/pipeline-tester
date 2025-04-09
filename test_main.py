import pytest
from main import A, B


def test_volume():
    #Arrange
    expected:float = 30
    a: A = A()
    
    #Action
    vol:float = a.volume(5,6)
    #Assert
    assert vol == expected , "height 5 * area 6 must be 30"


def test_volume_with_negative_height():
    #Arrange
    a: A = A()
    
    #Assert
    with pytest.raises(ValueError,match="Height and area must be non-negative"):
        a.volume(-1,6)



def test_get_volume():
    expected:str = f"23.85 is the volume"  
    b:B = B()
    vol_string:str = b.get_volume(4.5,5.3)

    assert vol_string == expected, "The output text has to be 23.85 is the volume"