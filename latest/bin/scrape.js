const fs = require("fs");

const proxies = [];
const output_file = "proxy.txt";

if (fs.existsSync(output_file)) {
  fs.unlinkSync(output_file);
  console.log(`Updating '${output_file}'`);
}

const raw_proxy_sites = [
  "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/main/connect.txt",
  "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/proxy.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
  "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
  "https://raw.githubusercontent.com/yogendratamang48/ProxyList/master/proxies.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/master/proxies.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/unchecked.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/https.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/proxylist.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
];

async function fetchProxies() {
  for (const site of raw_proxy_sites) {
    try {
      const response = await fetch(site);
      if (response.ok) {
        //console.log(`success: ${site}`);
        const data = await response.text();
        const lines = data.split("\n");
        for (const line of lines) {
          if (line.includes(":")) {
            const [ip, port] = line.split(":", 2);
            proxies.push(`${ip}:${port}`);
          }
        }
      } else {
        //console.log(`skip: ${site}`);
      }
    } catch (error) {
      //console.error(`skip: ${site}`);
    }
  }

  fs.writeFileSync(output_file, proxies.join("\n"));
  fs.readFile(output_file, "utf8", (err, data) => {
    if (err) {
      console.error("Error:", err);
      return;
    }
    const proxies = data.trim().split("\n");
    const totalProxies = proxies.length;
    console.log(`success updating ${totalProxies} proxy`);
  });
}
fetchProxies();
