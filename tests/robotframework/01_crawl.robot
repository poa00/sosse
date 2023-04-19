| *Settings* |
| Library | SeleniumLibrary
| Resource | common.robot

| *Test Cases* |
| Login
#|  | Open Browser | http://127.0.0.1/ | browser=Chrome | options=add_argument("--no-sandbox");add_argument("--headless");add_argument('--enable-precise-memory-info');add_argument('--disable-default-apps')
|  | Open Browser | http://127.0.0.1/ | browser=Firefox |  options=add_argument("--headless")
|  | Set Window Size | 1024 | 768
|  | Set Screenshot Directory | screenshots/
|  | Capture Element Screenshot | id=user_menu_button | user_menu_button.png
|  | Input Text | id=id_username | admin
|  | Input Text | id=id_password | admin
|  | Click Element | xpath=//form[@id='login-form']//input[@type='submit']
|  | Capture Page Screenshot | search.png
|  | Capture Element Screenshot | id=conf_menu_button | conf_menu_button.png
|  | Click Element | id=conf_menu_button
|  | Click Link | Administration
|  | Capture Page Screenshot | admin_ui.png

| Crawl a new URL
|  | Go To | http://127.0.0.1/admin/se/document/queue/
|  | Wait Until Element Is Visible | id=id_url
|  | Input Text | id=id_url | http://127.0.0.1/screenshots/website/index.html
|  | Click Element | xpath=//input[@value='Check and queue']
|  | Wait Until Page Contains | Create a new policy
|  | Capture Page Screenshot | crawl_new_url.png
|  | Click Element | xpath=//input[@value='Confirm']
|  | Wait Until Page Contains | Crawl status
|  | ${loc}= | Get Location
|  | Should Be Equal | ${loc} | http://127.0.0.1/admin/se/document/crawl_status/
|  | Page Should Not Contain | No crawlers running.
|  | Page Should Not Contain | exited
|  | Wait Until Page Contains | 4 documents to be recrawled | 2min
|  | Page Should Contain | idle
|  | Scroll Element Into View | id=result_list
|  | Capture Page Screenshot | crawl_status.png

| Crawl policies
|  | Go To | http://127.0.0.1/admin/se/crawlpolicy/
|  | Wait Until Element Is Visible | id=result_list
|  | Capture Page Screenshot | crawl_policy_list.png
|  | Click Element | xpath=//table[@id='result_list']//a[.='.*']
|  | Hilight | //fieldset[1]
|  | Scroll To Elem | //fieldset[1]
|  | Capture Page Screenshot | crawl_policy_decision.png

|  | Reload Page
|  | Hilight | //h2[.='Browser']/..
|  | Scroll To Elem | //h2[.='Browser']/..
|  | Capture Page Screenshot | crawl_policy_browser.png

|  | Reload Page
|  | Hilight | //h2[.='Updates']/..
|  | Scroll To Elem | //h2[.='Updates']/..
|  | Capture Page Screenshot | crawl_policy_updates.png

|  | Reload Page
|  | Execute Javascript | auth_fields = document.getElementById('authfield_set-group'); document.getElementsByTagName('fieldset')[3].append(auth_fields)
|  | Hilight | //h2[.='Authentication']/..
|  | Scroll To Elem | //h2[.='Authentication']/..
|  | Capture Page Screenshot | crawl_policy_auth.png

| Crawl on depth
|  | Reload Page
|  | Select From List By Label | id=id_condition | Depending on depth
|  | Capture Element Screenshot | //fieldset[1] | policy_on_depth.png
|  | Click Element | xpath=//input[@value="Save"]
|  | Go To | http://127.0.0.1/admin/se/document/queue/
|  | Wait Until Element Is Visible | id=id_url
|  | Input Text | id=id_url | http://127.0.0.1/screenshots/website/index.html
|  | Click Element | xpath=//input[@value='Check and queue']
|  | Hilight | id=id_crawl_depth
|  | Capture Page Screenshot | crawl_on_depth_add.png

|  | Go To | http://127.0.0.1/admin/se/crawlpolicy/add/
|  | Wait Until Element Is Visible | id=id_url_regex
|  | Input Text | id=id_url_regex | https://en.wikipedia.org/.*
|  | Input Text | id=id_crawl_depth | 2
|  | Capture Element Screenshot | //fieldset[1] | policy_all.png

| Documents
|  | Go To | http://127.0.0.1/admin/se/document/
|  | Wait Until Element Is Visible | id=result_list
|  | Capture Page Screenshot | documents_list.png
|  | ${doc_count}= | Get Element Count | xpath=//table[@id='result_list']/tbody/tr
|  | Should Be Equal As Numbers | ${doc_count} | 4

| Domain
|  | Go To | http://127.0.0.1/admin/se/domainsetting/
|  | Wait Until Element Is Visible | id=result_list
|  | ${dom_count}= | Get Element Count | xpath=//table[@id='result_list']/tbody/tr
|  | Should Be Equal As Numbers | ${dom_count} | 1
|  | Click Link | 127.0.0.1
|  | Capture Page Screenshot | domain_setting.png
