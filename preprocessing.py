import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, Normalizer
from time import time


def fillna_by_mean(df, ncolumns=[]):
    dff = df.loc[:, ncolumns] if len(ncolumns) > 0 else df
    ncounts = dff.isnull().sum()
    ncolumns = ncounts[ncounts > 0].keys()

    for column in ncolumns:
        df[column] = df[column].fillna(np.mean(df[column]))

    return df


def set_missing_feature(df, feature_name='field'):
    if df[feature_name].isnull().sum() == 0:
        return df
    process_df = df[[feature_name, 'reg_time', 'reg_capital', 'patent', 'trademark', 'copyright',
               'DFA', 'DFC', 'EFQ', 'EFC', 'IFTFQ', 'IFTFC', 'PFPFQ', 'PFPFC',
               'emp_num', 'asset', 'debt', 'op_income', 'main_income', 'total_profit',
               'net_profit', 'tax', 'total_equity']]

    known = process_df[process_df[feature_name].notnull()].values
    unkown = process_df[process_df[feature_name].isnull()].values

    X = known[:, 1:]

    y = known[:, 0]

    rfc = RandomForestClassifier(random_state=0, n_estimators=7, n_jobs=2)
    rfc.fit(X, y)

    predicted = rfc.predict(unkown[:, 1:])

    df.loc[df[feature_name].isnull(), feature_name] = predicted
    return df, rfc


def cat_to_int(df, feature_name=None):
    print('='*50)
    enc = LabelEncoder()
    label_encoder = enc.fit(df[feature_name])
    print('Catgorical classes: {}'.format(label_encoder.classes_))
    integer_classes = label_encoder.transform(label_encoder.classes_)
    print('Interger classes: {}'.format(integer_classes))
    print('='*50, '\n')
    df[feature_name] = label_encoder.transform(df[feature_name])
    return df


def cat_to_dummies(df, feature_name, prefix=''):
    print('='*50)
    # transform classes into inter values
    enc = LabelEncoder()
    label_encoder = enc.fit(df[feature_name])
    print('Catgorical classes: {}'.format(label_encoder.classes_))

    integer_classes = label_encoder.transform(label_encoder.classes_).reshape(-1, 1)
    print('Interger classes: {}'.format(integer_classes))

    enc = OneHotEncoder(categories='auto')
    one_hot_encoder = enc.fit(integer_classes)
    # First, convert classes to 0-(N-1) integers using label_encoder
    num_of_rows = df.shape[0]
    t = label_encoder.transform(df[feature_name]).reshape(num_of_rows, 1)
    # Second, create a sparse matrix with three columns,  each one indicating if the instance belongs to the class
    new_feature = one_hot_encoder.transform(t)
    new_feature = pd.DataFrame(new_feature.toarray(), columns=label_encoder.classes_)
    new_feature = new_feature.add_prefix(prefix)
    # Add the new features to titanic_X
    df = pd.concat([df, new_feature], axis=1)
    # Eliminate converted columns
    df = df.drop(feature_name, axis=1)
    print('='*50, '\n')
    return df


def merge_all_tables(base, knowledge, money, year_report):
    # Preprocessing
    money['year'] = money['year'].fillna(method='bfill')
    year_report['year'] = year_report['year'].fillna(method='bfill')

    # Merge table `money` and table `year_report`
    money_and_year_report = pd.merge(money, year_report, how='outer')
    money_and_year_report = fillna_by_mean(money_and_year_report)

    # Groupby property `ID` and drop `year` column
    money_and_year_report_mean = money_and_year_report.groupby(['ID']).mean()
    money_and_year_report_mean.drop('year', axis=1, inplace=True)

    # Merge table `base` and table `knowledege`
    base_and_knowledge = pd.merge(base, knowledge, how='outer')

    # Merge all tables
    money_and_year_report_mean = money_and_year_report_mean.reset_index()
    full_data = pd.merge(base_and_knowledge, money_and_year_report_mean, how='outer')

    full_data = fillna_by_mean(full_data, ncolumns=money_and_year_report_mean.columns)
    if 'flag' in full_data.columns:
        full_data = full_data[['ID', '注册时间', '注册资本', '行业', '区域', '企业类型', '控制人类型', '控制人持股比例', 'flag',
           '专利', '商标', '著作权', '债权融资额度', '债权融资成本', '股权融资额度', '股权融资成本',
           '内部融资和贸易融资额度', '内部融资和贸易融资成本', '项目融资和政策融资额度', '项目融资和政策融资成本', '从业人数',
           '资产总额', '负债总额', '营业总收入', '主营业务收入', '利润总额', '净利润', '纳税总额', '所有者权益合计']]

        columns = ['ID', 'reg_time', 'reg_capital', 'field', 'area', 'company_type', 'controller_type',
                   'controller_share_ratio', 'flag', 'patent', 'trademark', 'copyright',
                   'DFA', 'DFC', 'EFQ', 'EFC', 'IFTFQ', 'IFTFC', 'PFPFQ', 'PFPFC',
                   'emp_num', 'asset', 'debt', 'op_income', 'main_income', 'total_profit',
                   'net_profit', 'tax', 'total_equity']
    else:
        full_data = full_data[['ID', '注册时间', '注册资本', '行业', '区域', '企业类型', '控制人类型', '控制人持股比例',
                               '专利', '商标', '著作权', '债权融资额度', '债权融资成本', '股权融资额度', '股权融资成本',
                               '内部融资和贸易融资额度', '内部融资和贸易融资成本', '项目融资和政策融资额度', '项目融资和政策融资成本', '从业人数',
                               '资产总额', '负债总额', '营业总收入', '主营业务收入', '利润总额', '净利润', '纳税总额', '所有者权益合计']]

        columns = ['ID', 'reg_time', 'reg_capital', 'field', 'area', 'company_type', 'controller_type',
                   'controller_share_ratio', 'patent', 'trademark', 'copyright',
                   'DFA', 'DFC', 'EFQ', 'EFC', 'IFTFQ', 'IFTFC', 'PFPFQ', 'PFPFC',
                   'emp_num', 'asset', 'debt', 'op_income', 'main_income', 'total_profit',
                   'net_profit', 'tax', 'total_equity']

    full_data.columns = columns
    return full_data


def fill_missing_values(full_data):
    """
    fill in the remaining missing values
    :param full_data:
    :return:
    """
    # 注册时间：众数填充
    full_data['reg_time'].fillna(full_data['reg_time'].mode()[0], inplace=True)
    full_data['reg_time'] = full_data['reg_time'].apply(lambda x: 2020 - x)

    # 注册资本: 平均数填充
    full_data['reg_capital'].fillna(np.mean(full_data['reg_capital']), inplace=True)

    # 控制人持股比例
    full_data['controller_share_ratio'].fillna(np.mean(full_data['controller_share_ratio']), inplace=True)

    # 专利: 0
    full_data['patent'].fillna(0, inplace=True)

    # 商标: 0
    full_data['trademark'].fillna(0, inplace=True)

    # 著作权: 0
    full_data['copyright'].fillna(0, inplace=True)

    full_data, rfc = set_missing_feature(full_data, 'field')
    full_data, rfc = set_missing_feature(full_data, 'area')
    full_data, rfc = set_missing_feature(full_data, 'company_type')
    full_data, rfc = set_missing_feature(full_data, 'controller_type')

    return full_data


def convert_cat(full_data):
    # 行业:
    full_data = cat_to_int(full_data, feature_name='field')
    # 区域:
    full_data = cat_to_int(full_data, feature_name='area')
    # 企业类型：
    full_data = cat_to_int(full_data, feature_name='company_type')
    # 控制人类型：
    full_data = cat_to_int(full_data, feature_name='controller_type')
    return full_data

def scaling(full_data):
    std_scaler = StandardScaler()
    rob_scaler = RobustScaler()
    mm_scaler = MinMaxScaler()
    normed_scaler = Normalizer()

    features = ['reg_time', 'reg_capital', 'DFA', 'DFC', 'EFQ', 'EFC', 'IFTFQ', 'IFTFC', 'PFPFQ', 'PFPFC', 'emp_num',
         'asset', 'debt', 'op_income', 'main_income', 'total_profit', 'net_profit', 'tax', 'total_equity']
    for feature in features:
        full_data['scaled_'+feature] = std_scaler.fit_transform(full_data[feature].values.reshape(-1, 1))
        
    full_data.drop(
        ['ID', 'reg_time', 'reg_capital', 'DFA', 'DFC', 'EFQ', 'EFC', 'IFTFQ', 'IFTFC', 'PFPFQ', 'PFPFC', 'emp_num',
         'asset', 'debt', 'op_income', 'main_income', 'total_profit', 'net_profit', 'tax', 'total_equity'], axis=1,
        inplace=True)
    return full_data

def preprocessing(df_list=None, train=True, test=False, scaled=True, cat_converted=True):
    if test:
        base = pd.read_csv('./data/base_verify1.csv')
        knowledge = pd.read_csv('./data/knowledge_verify1.csv')
        money = pd.read_csv('./data/money_report_verify1.csv')
        year_report = pd.read_csv('./data/year_report_verify1.csv')

    if train:
        base = pd.read_csv('./data/base_train_sum.csv')
        knowledge = pd.read_csv('./data/knowledge_train_sum.csv')
        money = pd.read_csv('./data/money_report_train_sum.csv')
        year_report = pd.read_csv('./data/year_report_train_sum.csv')

    if not train and not test:
        base, knowledge, money, year_report = df_list[0], df_list[1], df_list[2], df_list[3]

    # Merge tables and fill in the missing values
    t0 = time()
    full_data = merge_all_tables(base, knowledge, money, year_report)
    full_data = fill_missing_values(full_data)
    t1 = time()
    print('Fill in missing values takes {} s'.format(t1 - t0))

    # Scaling
    if scaled:
        t0 = time()
        full_data = scaling(full_data)
        t1 = time()
        print('Scaling takes {} s'.format(t1 - t0))

    # Convert catagorical data
    if cat_converted:
        t0 = time()
        full_data = convert_cat(full_data)
        t1 = time()
        print('Convert catagorical data takes {} s'.format(t1 - t0))

    # print(full_data.head())
    return full_data


# if __name__ == '__main__':
#     # Read Training Data
#     preprocessing()

    # print(full_data.isnull().sum())
