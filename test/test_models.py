import sys
sys.path.append(".")

from src.picbedshower.model.models import PicBedModel

if __name__ == '__main__':
    tmp = PicBedModel(owner="asd", repo="repo")
    print(tmp)
    print(tmp.getcontenturl("test"))