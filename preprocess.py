 # -*- coding: utf-8 -*-
import getopt
import sys
import numpy as np 
import re


TRAINVAL_DATA_PATH = './data/train11w.data'
TEST_DATA_PATH = './data/test5w.data'
TRAINVAL_FEATURES_PATH = './features/trainval' 
TEST_FEATURES_PATH = './features/test'


def onehot(n, k):
    code = np.zeros(n)
    code[k] = 1
    return code
    
        
def handle_qq_md5(s):
    if not (s.isalnum() and len(s) == 32):
        print 'illegal qq_md5: %s' % s
        sys.exit(2)
    return np.zeros(shape=(0,))

    
def handle_gender(s):
    '''
    GENDER_UNKNOWN = 0;  // 性别未知
    GENDER_MALE = 1;  // 男
    GENDER_FEMALE = 2;  // 女
    '''
    gender = int(s)
    if gender not in (0, 1, 2):
        print 'illegal gender: %s' % s
        sys.exit(2)
    return onehot(3, gender)
    
    
def handle_year(s):
    year = int(s)
    if not 1900 <= year <= 2016:
        print 'illegal year: %s' % s
        sys.exit(2)
    return year


def handle_surf_scene(s):
    '''
    SURF_SCENE_PUBLIC = 1;  // 公共场所
    SURF_SCENE_HOME = 2;  // 家庭
    SURF_SCENE_OFFICE = 3;  // 办公
    SURF_SCENE_SCHOOL = 4;  // 学校
    SURF_SCENE_WIRELESS = 5;  // 无线上网
    '''
    surf_scene = int(s)
    if surf_scene not in (1, 2, 3, 4, 5):
        print 'illegal surf_scene: %s' % s
        sys.exit(2)
    return onehot(5, surf_scene - 1)


def handle_marriage_status(s):
    '''
    MARRIAGE_STATUS_UNKNOWN = 0;  // 未知
    MARRIAGE_STATUS_SINGLE = 1;  // 单身
    MARRIAGE_STATUS_HAVE_BABY = 2;  // 育儿
    MARRIAGE_STATUS_NEWLY_WEDS = 3;  // 新婚
    MARRIAGE_STATUS_IN_LOVE = 4;  // 恋爱
    MARRIAGE_STATUS_HAVE_KID = 5;  // 子女教育
    MARRIAGE_STATUS_MARRIED = 6;  // 已婚
    MARRIAGE_STATUS_SECRET = 7;  // 保密
    MARRIAGE_STATUS_ENGAGED = 8;  // 已订婚
    MARRIAGE_STATUS_SEPARATED = 9;  // 分居
    MARRIAGE_STATUS_DIVORCED = 10;  // 离异
    '''
    marriage_status = int(s)
    if not (0 <= marriage_status <= 10):
        print 'illegal marriage_status: %s' % s
        sys.exit(2)
    return onehot(11, marriage_status)


def handle_education(s):
    '''
    EDUCATION_UNKNOWN = 0;  // 学历未知
    EDUCATION_DOCTOR = 1;  // 博士
    EDUCATION_MASTER = 2;  // 硕士
    EDUCATION_COLLEGE = 3;  // 大学生
    EDUCATION_HIGH_SCHOOL = 4;  // 高中
    EDUCATION_MIDDLE_SCHOOL = 5;  // 初中
    EDUCATION_PRIMARY_SCHOOL = 6;  // 小学
    '''
    education = int(s)
    if not (0 <= education <= 6):
        print 'illegal education: %s' % s
        sys.exit(2)
    return onehot(7, education)


def handle_profession(s):
    '''
    PROFESSION_UNKNOWN = 0;  // 用户职业未知
    PROFESSION_COMPUTER = 1;  // 计算机/互联网/通信/电子
    PROFESSION_MARKETING = 2;  // 销售/客服/技术支持
    PROFESSION_FINANCE = 3;  // 会计/金融/银行/保险
    PROFESSION_MANUFACTURING = 4;  // 生产/营运/采购/物流
    PROFESSION_HEALTHY = 5;  // 生物/制药/医疗/护理
    PROFESSION_MEDIA = 6;  // 广告/市场/媒体/艺术
    PROFESSION_ARCHITECTURE = 7;  // 建筑/房地产
    PROFESSION_ADMINISTRATION = 8;  // 人事/行政/高级管理
    PROFESSION_EDUCATION = 9;  // 咨询/法律/教育/科研
    PROFESSION_SERVICE = 10;  // 服务业
    PROFESSION_SERVANTS = 11;  // 公务员/翻译
    PROFESSION_ENGINEERING = 12;  // 工程行业
    '''
    profession = int(s)
    if not (0 <= profession <= 12):
        print 'illegal profession: %s' % s
        sys.exit(2)
    return onehot(13, profession)


def handle_creative_id(s):
    return np.zeros(shape=(0, ))
    
 
def handle_category_id(s):
    return np.zeros(shape=(0, ))
    
    
def handle_series_id(s):
    return np.zeros(shape=(0, ))
    
    
def handle_advertiser_id(s):
    return np.zeros(shape=(0, ))


def handle_product_type(s):
    '''
    see producttype.png
    '''
    product_type = int(s)
    if not (product_type in (1000, 10001) or 1 <= product_type <= 34):
        print 'illegal product_type: %s' % s
        #return None
        sys.exit(2)
    if product_type >= 1000:
        product_type -= (1000 - 35)
    return onehot(36, product_type - 1)


def handle_product_id(s):
    return np.zeros(shape=(0, ))
    
    
def handle_image_url(s):
    return np.zeros(shape=(0, ))


def handle_page_url(s):
    return np.zeros(shape=(0, ))
        

def handle_imp_time(s):
    imp_time = int(s)
    if not (0 <= imp_time <= 1467302400):
        print 'illegal imp_time: %s' % s
        sys.exit(2)
    return np.zeros(shape=(0, ))


def handle_pos_id(s):
    '''
    288235913187546319
    72063131073762511
    144120725111690447
    216178319149618383]
    '''
    pos_id = int(s)
    values = [288235913187546319, 72063131073762511, 144120725111690447, 216178319149618383]
    if pos_id not in values:
        print 'illegal pos_id: %s' % s
        sys.exit(2)
    return onehot(4, values.index(pos_id))
        

def handle_click_num(s):
    click_num = int(s)
    if click_num not in (0, 1):
        print 'illegal click_num: %s' % s
        sys.exit(2) 
    return click_num   


def convert(category, inputPath, outputPath):
    print 'converting ' + inputPath
    features = []
    labels = [] if category == 'trainval' else None
    urlReg = re.compile(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")
    
    for (i, line) in enumerate(open(inputPath)):
        line = line.strip()
        feature_vector = []
        fields = line.split()
        urlIndice = []
        for (i, s) in enumerate(fields):
            if urlReg.match(s) != None:
                urlIndice.append(i)
        assert len(urlIndice) <= 2
        feature_vector.append(handle_qq_md5(fields[0]))
        feature_vector.append(handle_gender(fields[1]))
        feature_vector.append(handle_year(fields[2]))
        feature_vector.append(handle_surf_scene(fields[3]))
        feature_vector.append(handle_marriage_status(fields[4]))
        feature_vector.append(handle_education(fields[5]))
        feature_vector.append(handle_profession(fields[6]))
        feature_vector.append(handle_creative_id(fields[7]))
        feature_vector.append(handle_category_id(fields[8]))
        feature_vector.append(handle_series_id(fields[9]))
        feature_vector.append(handle_advertiser_id(fields[10]))
        feature_vector.append(handle_product_type(fields[11]))
        feature_vector.append(handle_product_id(fields[12] if urlIndice[0] != 12 else ''))
        feature_vector.append(handle_image_url(fields[urlIndice[0]]))
        feature_vector.append(handle_page_url(fields[urlIndice[1]] if len(urlIndice) > 1 else ''))
        feature_vector.append(handle_imp_time(fields[-3] if category == 'trainval' else fields[-2]))
        feature_vector.append(handle_pos_id(fields[-2] if category == 'trainval' else fields[-1]))
        features.append(np.hstack(feature_vector))
        if category == 'trainval':
            labels.append(handle_click_num(fields[-1]))
   
    features = np.vstack(features)
    print '%dx%d feature matrix saved to %s' % (features.shape[0], features.shape[1], outputPath + '_features.npy')
    np.save(outputPath + '_features', features)
    if category == 'trainval':
        labels = np.vstack(labels).flatten()
        print '%d label vector saved to %s' % (labels.shape[0], outputPath + '_labels.npy')
        np.save(outputPath + '_labels', labels)

    
        


if __name__ == '__main__':

    convert('trainval', TRAINVAL_DATA_PATH, TRAINVAL_FEATURES_PATH)
    convert('test', TEST_DATA_PATH, TEST_FEATURES_PATH)
