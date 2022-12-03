"""
Steps:
1. run updateCompanyInfo
2. run updateMarketInfo
3. run generateDataset
4. build models & save model
"""
from scripts.buildModels import update_models
from scripts.dumpDataToS3 import dump_and_upload_data
from scripts.generateDataset import update_dataset
from scripts.updateCompanyInfo import update_company_info
from scripts.updateMarketInfo import update_market_info
from scripts.updatePrediction import update_prediction

if __name__ == '__main__':
    # update_company_info()
    # update_market_info()
    # update_dataset()
    update_models(save_model=True, dump_performance=True)
    # update_prediction()
    # dump_and_upload_data()
