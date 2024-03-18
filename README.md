# WebSiteInfo

本脚本用于个人打点收集资产的插件使用，作为资产收集的补充

脚本简单、内容肤浅

## 脚本逻辑:

	爬取指定url链接
	
	过滤link

		设置了4个子集，url_subdomain、subdomain、url_ip、ip
	 
		如果是ip
	 
			直接将link填入url_ip以及ip中
	  
		如果是domain
	 
			判断link是否包含login、admin、sign、auth关键字
	  
			判断是否与输入 URL 具有相同主域名
	  
			判断是否同备案（需要根据实际情况实现）
	  
			通过任一均填入url_subdomain以及subdomain中


后续如何利用这些子集就看个人需求

![image](https://github.com/nex121/websiteinfo/assets/29255605/ba61c559-7855-40fb-a8f9-d4d832f83c7a)
