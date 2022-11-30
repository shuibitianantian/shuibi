"""
Steps:
1. run updateCompanyInfo
2. run updateMarketInfo
3. run generateDataset
4. build models & save model
"""
from scripts.generateDataset import update_dataset
from scripts.updateCompanyInfo import update_company_info
from scripts.updateMarketInfo import update_market_info

if __name__ == '__main__':
    update_company_info()
    update_market_info()
    update_dataset()
