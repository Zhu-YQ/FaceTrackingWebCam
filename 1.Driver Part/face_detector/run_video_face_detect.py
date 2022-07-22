import cv2

from vision.ssd.config.fd_config import define_img_size

define_img_size(480)  # must put define_img_size() before 'import create_mb_tiny_fd, create_mb_tiny_fd_predictor'

from vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor

label_path = "model/voc-model-labels.txt"

cap = cv2.VideoCapture(0)  # capture from camera

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)
test_device = "cuda:0"

candidate_size = 1000
threshold = 0.7

model_path = "model/version-RFB-320.pth"
net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=test_device)
predictor = create_Mb_Tiny_RFB_fd_predictor(net, candidate_size=candidate_size, device=test_device)

net.load(model_path)

while True:
    ret, orig_image = cap.read()
    if orig_image is None:
        print("end")
        break
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

    boxes, labels, probs = predictor.predict(image, candidate_size / 2, threshold)

    for i in range(boxes.size(0)):
        box = boxes[i, :]
        label = f" {probs[i]:.2f}"
        cv2.rectangle(orig_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 4)
        print('left:', int(box[0]), 'top:', int(box[1]), 'right:', int(box[2]), 'bottom:', int(box[3]))
    orig_image = cv2.resize(orig_image, None, None, fx=0.8, fy=0.8)
    cv2.imshow('annotated', orig_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
