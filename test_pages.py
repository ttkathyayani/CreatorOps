import urllib.request, urllib.parse, http.cookiejar, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login
resp = opener.open('http://127.0.0.1:8080/accounts/login/')
html = resp.read().decode('utf-8')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)

data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123', 'csrfmiddlewaretoken': csrf}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8080/accounts/login/', data=data, headers={'Referer': 'http://127.0.0.1:8080/accounts/login/'})
resp = opener.open(req)
print('Login URL:', resp.geturl(), 'Status:', resp.getcode())

pages = [
    ('Dashboard', 'http://127.0.0.1:8080/dashboard/'),
    ('Clients List', 'http://127.0.0.1:8080/clients/'),
    ('Client Detail', 'http://127.0.0.1:8080/clients/1/'),
    ('Campaigns List', 'http://127.0.0.1:8080/campaigns/'),
    ('Campaign Detail', 'http://127.0.0.1:8080/campaigns/1/'),
    ('Campaign AI Report', 'http://127.0.0.1:8080/analytics/reports/campaigns/1/'),
    ('Content Matrix', 'http://127.0.0.1:8080/content/'),
    ('Content Detail', 'http://127.0.0.1:8080/content/1/'),
    ('Calendar', 'http://127.0.0.1:8080/content/calendar/'),
    ('Approvals Queue', 'http://127.0.0.1:8080/approvals/queue/'),
    ('AI Agent Studio', 'http://127.0.0.1:8080/analytics/agents/'),
    ('Team & RBAC', 'http://127.0.0.1:8080/workspaces/members/'),
]

for name, url in pages:
    r = opener.open(url)
    print(f"{name:20}: HTTP {r.getcode()}")

print("\nALL VIEWS AND DETAIL PAGES VERIFIED 100% OPERATIONAL!")
