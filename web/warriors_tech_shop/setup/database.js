const sqlite = require('sqlite-async');

class Database {
    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
    }

    async connect() {
        this.db = await sqlite.open(this.db_file);
    }


    async migrate() {
        var flag = process.env.flag

        this.db.exec(`
        DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT  NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL,
                role       VARCHAR(255) NOT NULL,
                bank       REAL NOT NULL
            );
        `);

        this.db.exec(`
        DROP TABLE IF EXISTS items;
        CREATE TABLE IF NOT EXISTS items (
            id            INTEGER NOT  NULL PRIMARY KEY AUTOINCREMENT,
            name          VARCHAR(255) NOT NULL UNIQUE,
            description   VARCHAR(255) NOT NULL,
            image         VARCHAR(255) NOT NULL,
            price         REAL NOT NULL
        );
        INSERT INTO items (name, description, image, price) VALUES
            ('Cipher Keys', 'These are special encryption keys that can unlock hidden data caches or decrypt sensitive information crucial to dismantling Project Echo.', 'cipher_keys.png', 49.99),
            ('Virtual Reality Cloaks', 'Advanced cloaking devices that allow hackers to disguise their presence in virtual environments, making it harder for OrionTech''s surveillance systems to track them', 'virtual_reality_cloaks.png', 420.69),
            ('Neural Interface Chips', 'Implantable chips that enhance hackers'' cognitive abilities, granting them faster processing speeds and improved problem-solving capabilities when navigating through complex digital landscapes.', 'neural_interface_chips.png', 300),
            ('Echo Disruptor Grenades', 'Tactical grenades designed to disrupt Project Echo''s communication channels, temporarily disabling surveillance drones and security systems within a specific radius.', 'echo_disruptor_grenades.png', 80),
            ('AI Ally Modules', 'Modular AI companions programmed to assist hackers in their missions, providing real-time analysis, reconnaissance, and strategic advice during critical operations.', 'ai_ally_modules.png', 499.99),
            ('Cybernetic Implants', 'Enhancements that grant hackers augmented abilities, such as enhanced reflexes, heightened senses, or even limited telepathic communication within the digital realm.', 'cybernetic_implants.png', 699.99),
            ('Stealth Hacking Tools', 'Specialized software and hardware kits that enable silent infiltration and covert data extraction from OrionTech''s secure networks without triggering alarms.', 'stealth_hacking_tools.png', 120),
            ('OrionTech Data Scramblers', 'Devices capable of scrambling OrionTech''s data transmissions, making it difficult for them to coordinate their operations effectively or gather intelligence on the Andromeda Initiative''s activities.', 'orion_tech_data_scramblers.png', 99.99),
            ('Cyberpunk Fashion', 'Stylish attire designed to blend in with the cyberpunk aesthetic of Cyprus, providing both functionality and flair for hackers navigating the streets and virtual realms alike.', 'cyberpunk_fashion.png', 50),
            ('Super Secret Flag', '${flag}', 'flag.png', 31337.01);
        `);

        return;
    }

   
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

    async register(user, pass, role, bank) {
      return new Promise(async(resolve, reject) => {
          try {
              let stmt = await this.db.prepare('insert into users (username, password, role, bank) values (?, ?, ?, ?)');
              resolve(await stmt.get(user, pass, role, bank));
          } catch (e) {
              reject(e);
          }
      });
  }

   async user_exists(user) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ?');
                let row = await stmt.get(user);
                resolve(row !== undefined);
            } catch(e) {
                reject(e);
            }
        });
    }

    async get_user(id) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM users WHERE id = ?');
                resolve(await stmt.get(id));
            } catch(e) {
                reject(e);
            }
        });
    }

    async update_balance(id, balance) {
        return new Promise(async (resolve, reject) => {
            await this.db.run("BEGIN TRANSACTION");
            try {        
                let stmt = await this.db.prepare('update users set bank = ? where id = ?');
                await stmt.run(balance, id);
                await stmt.finalize();
                await this.db.run("COMMIT");
                resolve();
            } catch(e) {
                await this.db.run("ROLLBACK");
                reject(e);
            }
        });
    }

    async items() {
        return new Promise(async(resolve, reject) => {
            try {
                const items = await this.db.all('SELECT * FROM items');
                resolve(items);
            } catch (e) {
                reject(e);
            }
        });
    }

    async item(id) {
        return new Promise(async(resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM items WHERE id = ?');
                resolve(await stmt.get(id));
            } catch (e) {
                reject(e);
            }
        });
    }

}

module.exports = Database;