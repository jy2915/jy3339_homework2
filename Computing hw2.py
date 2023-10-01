#!/usr/bin/env python
# coding: utf-8

# # Q1-1

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
# import necessary libraries which we used in class to do web crawling


# In[2]:


seed_url = 'https://press.un.org/en'
all_url = [seed_url]
seen = [seed_url]
opened = []
release = []

while len(all_url)>0 and len(release) <10:
    curr_url = all_url.pop(0) # take out the first url
    try:
        print(f'Current Url: {curr_url}')
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'}) # we crawl the same type of page as we did in class
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
        
    except:
        print(f'Unable To Access: {curr_url}')
        continue
    
    soup = BeautifulSoup(webpage) # arrange in nice soup format
    
    for tag in soup.find_all('a', href = True): # find all urls
        childUrl = tag['href'] # get this url
        o_childurl = childUrl # save the original o_childurl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url in childUrl and childUrl not in seen:
            print(f'Get A New childurl: {childUrl}')
            all_url.append(childUrl)
            seen.append(childUrl)
        else:
            print(f'Abandoning url: {childUrl}')
    
    # see if curr_url is a press release
    press_release_tag = soup.find('a', href='/en/press-release', hreflang='en',string='Press Release')
    
    if press_release_tag != None:
        print(f'Current Url {curr_url} is a PRESS RELEASE!')
        release.append(curr_url)

print('Here are the first 10 press release urls found!')
for release_url in release:
    print(release_url)
    


# In[3]:


release


# # Q1-2

# In[4]:


from tqdm import tqdm

seed_url = 'https://www.europarl.europa.eu/news/en/press-room'
all_url = [seed_url]
seen = [seed_url]
opened = []
release = []

pbar = tqdm(desc="Scraping URLs", unit="URL", position=0, leave=True)

while all_url and len(release) < 10:
    all_url = sorted(all_url, key=lambda s: 'crisis' not in s.lower()) # sort the urls placing those more likely to include crisis in front
    
    curr_url = all_url.pop(0)
    
    try:
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except:
        continue

    soup = BeautifulSoup(webpage, 'html.parser')
    
    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url in childUrl and childUrl not in seen:
            all_url.append(childUrl)
            seen.append(childUrl)
    
    plenary_session_tag = soup.find('span', class_="ep_name", string='Plenary session')
    crisis_title_tag = any('crisis' in title_tag.text.lower() for title_tag in soup.find_all('title'))
    
    if plenary_session_tag and crisis_title_tag:
        release.append(curr_url)
        
    pbar.set_description(f"all_url: {len(all_url)}: [{all_url[:5]}] , seen: {len(seen)}, opened: {len(opened)}, release: {len(release)}: {release}")
    pbar.update(1)  # Manually update the progress bar by 1

pbar.close()

print('Here are the first 10 press release about plenary session about crisis URLs found!')
for release_url in release:
    print(release_url)


# # Q2

# https://github.com/jy2915/jy3339_homework2.git

# ![image.png](attachment:image.png)

# In[ ]:




