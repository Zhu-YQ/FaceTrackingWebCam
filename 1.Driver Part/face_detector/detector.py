from .vision.ssd.config.fd_config import define_img_size
define_img_size(480)  # must put define_img_size() before 'import create_mb_tiny_fd, create_mb_tiny_fd_predictor'
from .vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor


class FaceDetector:
    MODEL_PATH = "face_detector/model/version-RFB-320.pth"
    LABEL_PATH = "face_detector/model/voc-model-labels.txt"

    def __init__(self):
        self.class_names = [name.strip() for name in open(FaceDetector.LABEL_PATH).readlines()]
        device = "cuda:0"

        self.candidate_size = 1000
        self.threshold = 0.7

        self.net = create_Mb_Tiny_RFB_fd(len(self.class_names), is_test=True, device=device)
        self.predictor = create_Mb_Tiny_RFB_fd_predictor(self.net, candidate_size=self.candidate_size, device=device)
        self.net.load(FaceDetector.MODEL_PATH)

    def predict(self, img):
        return self.predictor.predict(img, self.candidate_size / 2, self.threshold)

    def getFaceCP(self, img):
        result = self.predict(img)
        if result is None:
            return None
        boxes, labels, probs = result

        # 获取全部预测框与面积
        box_list = []
        area_list = []

        for i in range(boxes.size(0)):
            box = boxes[i, :]
            left = int(box[0])
            top = int(box[1])
            right = int(box[2])
            bottom = int(box[3])
            box_list.append([left, top, right, bottom])

            area = (bottom - top) * (right - left)
            area_list.append(area)

        if len(area_list) != 0:
            max_area = max(area_list)
            # 选取面积最大的预测框
            for i in range(len(area_list)):
                if area_list[i] == max_area:
                    # 传感器数据
                    box = box_list[i]
                    left = int(box[0])
                    top = int(box[1])
                    right = int(box[2])
                    bottom = int(box[3])
                    cp = (int((right + left) / 2), int((bottom + top) / 2))
                    return cp, left, top, right, bottom

