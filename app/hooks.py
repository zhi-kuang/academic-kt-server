from transformers import AutoTokenizer, AutoModel
from globals import global_vals
import os, sys
import torch

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

def load_chat_glm_6b():
    model_conf = global_vals['config']['model_conf']

    global_vals['tokenizer'] = AutoTokenizer.from_pretrained(model_conf['CHATGLM_6B_PATH'], trust_remote_code=True)
    global_vals['model'] = AutoModel.from_pretrained(model_conf['CHATGLM_6B_PATH'], trust_remote_code=True).half().cuda(model_conf['GPU_ID']).eval()

def load_SAKT():
    cuda = '0'
    if torch.cuda.is_available():
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    # 加载模型
    model = torch.load('model.pt')
    model.to(device)
    global_vals['model'] = model


def run_hooks():
    """
    项目启动前的加载项，都可以在这里执行
    """
    # load_chat_glm_6b()
    load_SAKT()

if __name__ == '__main__':
    run_hooks()
