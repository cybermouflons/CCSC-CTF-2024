const sqlite = require('sqlite-async');
const crypto = require('crypto');

const generateRandomData = () => {
    const cities = ['Nicosia', 'Limassol', 'Larnaca', 'Famagusta', 'Paphos'];
    const operatingSystems = ['Windows', 'Linux', 'Android', 'iOS'];

    // Generate random IP address
    const generateRandomIpAddress = () => {
        const octets = Array.from({ length: 4 }, () => Math.floor(Math.random() * 256));
        return octets.join('.');
    };

    // Generate random data and insert into the systems table
    const ip_address = generateRandomIpAddress();
    const country = 'Cyprus';
    const city = cities[Math.floor(Math.random() * cities.length)];
    const os = operatingSystems[Math.floor(Math.random() * operatingSystems.length)];

    return { ip_address, country, city, os }
};


class Database {
    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
    }

    async connect() {
        this.db = await sqlite.open(this.db_file);
    }

    async migrate() {
        var username = process.env.admin_username
        var password = process.env.admin_password + crypto.randomBytes(3).toString("hex")

        // Users Table Init
        this.db.exec(`
        DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT  NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL,
                is_admin   tinyint NOT NULL
            );
            INSERT INTO users (username, password, is_admin) VALUES
                ('${username}', '${password}', 1)
        `);

        this.db.exec(`
        DROP TABLE IF EXISTS systems;
            CREATE TABLE IF NOT EXISTS systems (
                id           INTEGER NOT  NULL PRIMARY KEY AUTOINCREMENT,
                ip_address   VARCHAR(255) NOT NULL UNIQUE,
                country      VARCHAR(255) NOT NULL,
                city         VARCHAR(255) NOT NULL,
                os           VARCHAR(255) NOT NULL
            );
        `);

        
        for (let i = 1; i <= 30; i++) {
            const { ip_address, country, city, os } = generateRandomData();
            this.db.exec(`
            INSERT INTO systems (ip_address, country, city, os) VALUES
                ('${ip_address}', '${country}', '${city}', '${os}');
            `)
        }

        return;
    }

    // User Functions
    async login(user, pass) {
        return new Promise(async(resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM users WHERE username = ? and password = ?');
                resolve(await stmt.get(user, pass));
            } catch (e) {
                reject(e);
            }
        });
    }

    async search(ip_address) {
        return new Promise(async(resolve, reject) => {
            try {
                let system = await this.db.all(`SELECT * FROM systems WHERE ip_address = '${ip_address}'`);
                resolve(system);
            } catch (e) {
                reject(e)
            }
        });
    }

    async getSystems() {
        return new Promise(async(resolve, reject) => {
            try {
                const items = await this.db.all('SELECT * FROM systems');
                resolve(items);
            } catch (e) {
                reject(e);
            }
        });
    }

}

module.exports = Database;