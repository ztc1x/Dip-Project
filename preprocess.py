 # -*- coding: utf-8 -*-
import getopt
import sys
import numpy as np 
import re
from progressbar import  Bar, Percentage, ProgressBar
import pickle
from datetime import datetime
import cPickle
from scipy.sparse import csr_matrix
import os
from jieba import posseg
from collections import OrderedDict
from time import clock


TRAINVAL_DATA_PATH = './data/train11w.data'
TEST_DATA_PATH = './data/test5w.data'
TRAINVAL_FEATURES_PATH = './features/trainval' 
TEST_FEATURES_PATH = './features/test'

qq_md5_list = pickle.load(open('qq_md5.pickle', 'rb'))
creative_id_list = pickle.load(open('creative_id.pickle', 'rb'))
category_id_list = pickle.load(open('category_id.pickle', 'rb'))
category_id_level_1_list = pickle.load(open('category_id_level_1.pickle', 'rb'))
category_id_level_2_list = pickle.load(open('category_id_level_2.pickle', 'rb'))
category_id_level_3_list = pickle.load(open('category_id_level_3.pickle', 'rb'))
advertiser_id_list = pickle.load(open('advertiser_id.pickle', 'rb'))
product_id_list = pickle.load(open('product_id.pickle', 'rb'))
series_id_list = pickle.load(open('series_id.pickle', 'rb'))

# Variables for processing ad text
common_word_list = []
punctuation_list = []
max_info_ratio = 0
word_code_list = []
punctuation_code_list = []


def onehot(n, k):
    code = np.zeros(n)
    if 0 <= k < n:
        code[k] = 1
    return code
    
        
def handle_qq_md5(s):
    if not (s.isalnum() and len(s) == 32):
        print 'illegal qq_md5: %s' % s
        sys.exit(2)
    
    return np.zeros(shape=(1,))

    
def handle_gender(s):
    '''
    GENDER_MALE = 1;  // 男
    GENDER_FEMALE = 2;  // 女
    '''
    gender = int(s)
    if gender not in (1, 2):
        print 'illegal gender: %s' % s
        sys.exit(2)
    return onehot(2, gender - 1)
    
    
def handle_year(s):
    year = int(s)
    if not 1956 <= year < 2013:
        print 'illegal year: %s' % s
        sys.exit(2)
    age = None
    if 2001 < year:  #child
        age = 0
    elif 1995 < year:  #teenage
        age = 1
    elif 1985 < year:  #young
        age = 2
    else:
        age = 3
    return onehot(4, age)


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
    if not (1 <= marriage_status <= 10):
        print 'illegal marriage_status: %s' % s
        sys.exit(2)
    return onehot(10, marriage_status - 1)


def handle_education(s):
    '''
    EDUCATION_DOCTOR = 1;  // 博士
    EDUCATION_MASTER = 2;  // 硕士
    EDUCATION_COLLEGE = 3;  // 大学生
    EDUCATION_HIGH_SCHOOL = 4;  // 高中
    EDUCATION_MIDDLE_SCHOOL = 5;  // 初中
    EDUCATION_PRIMARY_SCHOOL = 6;  // 小学
    '''
    education = int(s)
    if not (1 <= education <= 6):
        print 'illegal education: %s' % s
        sys.exit(2)
    return onehot(6, education - 1)


def handle_profession(s):
    '''
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
    if not (1 <= profession <= 12):
        print 'illegal profession: %s' % s
        sys.exit(2)
    return onehot(12, profession - 1)


def handle_creative_id(s):
    creative_id = int(s)
    if creative_id not in creative_id_list:
        print 'illegal creative_id %s' % s
        return
        sys.exit(2)
    return onehot(len(creative_id_list), creative_id_list.index(creative_id))
    
 
def handle_category_id(s):
    category_id = int(s)
    if not (1 <= category_id <= 40521):
        print 'illegal category_id: %s' % s
        sys.exit(2)   
    level_1_id = None
    level_2_id = None
    level_3_id = None   
    if category_id < 100:
        level_1_id = category_id
    elif category_id < 10000:
        level_1_id = int(s[:-2])
        level_2_id = category_id
    else:
        level_1_id = 4
        level_2_id = int(s[:-2])
        level_3_id = category_id
    level_3_forbidden = 1 if level_1_id == 33 else 0
    level_2_forbidden = 1 if level_1_id in (18, 19, 20) or level_2_id in (201, 204, 205, 604, 607, 608, 609, 611, 1106) or level_3_id in (40302, 40501, 40514) else 0
    level_1_forbidden = 1 if level_2_forbidden or level_1_id == 21 or level_2_id in (207, 805, 1302) else 0
    forbidden = np.asarray([level_1_forbidden, level_2_forbidden, level_3_forbidden])
    return np.hstack((forbidden, 
                      onehot(len(category_id_level_1_list), category_id_level_1_list.index(level_1_id)),
                      onehot(len(category_id_level_2_list), category_id_level_2_list.index(level_2_id) if level_2_id else -1),
                      onehot(len(category_id_level_3_list), category_id_level_3_list.index(level_3_id) if level_3_id else -1)
                      ))

    
def handle_series_id(s):
    series_id = int(s)
    if series_id not in series_id_list:
        print 'illegal series_id %s' % s
        return
        sys.exit(2)
    return onehot(len(series_id_list), series_id_list.index(series_id))
    
    
def handle_advertiser_id(s):
    advertiser_id = int(s)
    if advertiser_id not in advertiser_id_list:
        print 'illegal advertiser_id %s' % s
        return
        sys.exit(2)
    return onehot(len(advertiser_id_list), advertiser_id_list.index(advertiser_id))


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
    product_id = int(s) if len(s) > 0 else -1
    if product_id != -1:
        if product_id not in product_id_list:
            print 'illegal product_id %s' % s
            return
            sys.exit(2)
        return onehot(len(product_id_list), product_id_list.index(product_id))
    else:
        return onehot(len(product_id_list), -1)
    
    
def handle_image_url(s):
    return np.zeros(shape=(1,))


def handle_page_url(s):
    return np.zeros(shape=(1,))
        

def handle_imp_time(s):
    imp_time = int(s)
    if not (0 <= imp_time <= 1467302400):
        print 'illegal imp_time: %s' % s
        sys.exit(2)
    dt = datetime.fromtimestamp(imp_time)
    return onehot(24, dt.hour)


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
    click_num = -1 if click_num == 0 else click_num
    return np.asarray([click_num])   

def dedupe_list(l):
    return list(OrderedDict.fromkeys(l))

def preprocess_ad_text():
    global common_word_list
    global punctuation_list
    global max_info_ratio
    global word_code_list
    global punctuation_code_list
    start_time = clock()
    f = open(TRAINVAL_DATA_PATH, 'r')
    train_ad_text = f.read()
    entries = train_ad_text.split('\n')
    f.close()
    f = open(TEST_DATA_PATH, 'r')
    test_ad_text = f.read()
    entries += test_ad_text.split('\n')
    f.close()
    text_list = []
    for entry in entries:
        if len(entry) > 15:
            text_list.append(entry.split('\t')[15])
    text_list = dedupe_list(text_list)
    segged_texts = []
    word_cnt_dict = dict()
    for text in text_list:
        words = posseg.cut(text)
        segged_text = []
        for word, flag in words:
            key = word + '||' + flag
            if key in word_cnt_dict:
                word_cnt_dict[key] += 1
            else:
                word_cnt_dict[key] = 1
            segged_text.append((word, flag))
        segged_texts.append(segged_text)
    word_tuples = []
    for key in word_cnt_dict.keys():
        word_flag = key.split('||')
        word_tuples.append((word_flag[0], word_flag[1], word_cnt_dict[key]))
    init_sorted_words = sorted(word_tuples, key=lambda word:word[2])
    sorted_words = []
    for item in init_sorted_words:
        if item[2] > 1:
            sorted_words.append(item)
    common_cnt = sorted_words[len(sorted_words)/2][2]
    common_word_list = []
    init_puntuation_list = []
    for item in sorted_words:
        if item[2] == common_cnt and item[1] != 'x':
            common_word_list.append((item[0], item[1]))
        if (item[1] == 'x' or item[1] == 'w') and item[2] > 3:
            punctuation_list.append((item[0], item[1]))
    print len(common_word_list)
    for segged_text in segged_texts:
        word_code = ''
        for common_word in common_word_list:
            if common_word in segged_text:
                word_code += '1'
            else:
                word_code += '0'
        word_code_list.append(word_code)
        punctuation_code = ''
        for punctuation in punctuation_list:
            if punctuation in segged_text:
                punctuation_code += '1'
            else:
                punctuation_code += '0'
        punctuation_code_list.append(punctuation_code)
    word_code_list = dedupe_list(word_code_list)
    punctuation_code_list = dedupe_list(punctuation_code_list)
    end_time = clock()
    print '--------------------------------'
    print 'Preprocessing of ad text done.'
    print 'Number of distinct ads: ' + str(len(text_list))
    print 'Number of words: ' + str(len(word_cnt_dict))
    print 'Number of common words: ' + str(len(common_word_list))
    print 'Number of word codes: ' + str(len(word_code_list))
    print 'Number of punctuationcodes: ' + str(len(punctuation_code_list))
    print 'Time elapsed: ' + str(end_time - start_time) + 's'
    print '--------------------------------'


def handle_ad_text(s):
    global common_word_list
    global punctuation_list
    global max_info_word_cnt
    global word_code_list
    global punctuation_code_list
    words = posseg.cut(s)
    segged_text = []
    for word, flag in words:
        segged_text.append((word, flag))
    word_code = ''
    punctuation_code = ''
    for common_word in common_word_list:
        if common_word in segged_text:
            word_code += '1'
        else:
            word_code += '0'
    for punctuation in punctuation_list:
        if punctuation in segged_text:
            punctuation_code += '1'
        else:
            punctuation_code += '0'
    info_cnt = 0
    for item in segged_text:
        if 'n' in item[1] or 'v' in item[1]:
            info_cnt += 1
    info_ratio = 50 * info_cnt / len(segged_text)
    #feature_vector = []
    #f1 = onehot(len(word_code_list), word_code_list.index(word_code))
    #f2 = onehot(len(punctuation_list), punctuation_code_list.index(punctuation_code))
    v = np.zeros(len(word_code_list) + len(punctuation_code_list) + 51)
    if word_code in word_code_list:
        v[word_code_list.index(word_code)] = 1
    else:
        print 'anomaly' + s
    if punctuation_code in punctuation_code_list:
        v[punctuation_code_list.index(punctuation_code) + len(word_code_list)] = 1
    else:
        print 'anomaly' + s
    v[len(punctuation_code_list) + len(word_code_list) + info_ratio] = 1
    return v


def audit(fields):
    if np.abs(int(fields[8])) > 50000:
        fields[8] = '1'
    
    
def convert(category, inputPath, outputPath):
    print 'converting ' + inputPath
    features = []
    labels = [] if category == 'trainval' else None
    urlReg = re.compile(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")
    
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(list(open(inputPath)))).start()
    for (i, line) in enumerate(open(inputPath)):
        pbar.update(i)
        line = line.strip()
        feature_vector = []
        fields = line.split('\t')
        audit(fields)
        urlIndice = []
        for (i, s) in enumerate(fields):
            if urlReg.match(s) != None:
                urlIndice.append(i)
        assert len(urlIndice) <= 2
        #feature_vector.append(handle_qq_md5(fields[0]))
        #feature_vector.append(handle_gender(fields[1]))
        #feature_vector.append(handle_year(fields[2]))
        #feature_vector.append(handle_surf_scene(fields[3]))
        #feature_vector.append(handle_marriage_status(fields[4]))
        #feature_vector.append(handle_education(fields[5]))
        #feature_vector.append(handle_profession(fields[6]))
        #feature_vector.append(handle_creative_id(fields[7]))
        #feature_vector.append(handle_category_id(fields[8]))
        #feature_vector.append(handle_series_id(fields[9]))
        #feature_vector.append(handle_advertiser_id(fields[10]))
        #feature_vector.append(handle_product_type(fields[11]))
        #feature_vector.append(handle_product_id(fields[12] if urlIndice[0] != 12 else ''))
        #feature_vector.append(handle_image_url(fields[urlIndice[0]]))
        feature_vector.append(handle_ad_text(fields[15]))
        #feature_vector.append(handle_page_url(fields[urlIndice[1]] if len(urlIndice) > 1 else ''))
        #feature_vector.append(handle_imp_time(fields[-3] if category == 'trainval' else fields[-2]))
        #feature_vector.append(handle_pos_id(fields[-2] if category == 'trainval' else fields[-1]))
        features.append(np.hstack(feature_vector))
        if category == 'trainval':
            labels.append(handle_click_num(fields[-1]))
   
    print ''
    features = np.vstack(features)
    print '%dx%d feature matrix saved to %s' % (features.shape[0], features.shape[1], outputPath + '_features.cPickle')
    cPickle.dump(csr_matrix(features), open(outputPath + '_features.cPickle', 'wb'))
    del features
    if category == 'trainval':
        labels = np.vstack(labels).flatten()
        print '%d label vector saved to %s' % (labels.shape[0], outputPath + '_labels.cPickle')
        cPickle.dump(labels, open(outputPath + '_labels.cPickle', 'wb'))
        

if __name__ == '__main__':

    os.system('mkdir features')
    preprocess_ad_text()
    convert('trainval', TRAINVAL_DATA_PATH, TRAINVAL_FEATURES_PATH)
    convert('test', TEST_DATA_PATH, TEST_FEATURES_PATH)
