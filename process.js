const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function run() {
    const files = fs.readdirSync('.');
    // 找出根目录下的图片文件，排除文件夹
    const images = files.filter(f => f.endsWith('.png') && fs.lstatSync(f).isFile());

    for (const file of images) {
        const dir = file; 
        if (!fs.existsSync(dir)) fs.mkdirSync(dir);
        
        try {
            await sharp(file)
                .resize(128, 128)
                .toFile(path.join(dir, 'icon.png'));
                
            fs.unlinkSync(file); // 转换成功后删除根目录原图
            console.log(`✅ Processed and cleaned: ${file}`);
        } catch (err) {
            console.error(`❌ Error processing ${file}:`, err);
        }
    }

    // 生成索引供网页显示
    const allDirs = fs.readdirSync('.').filter(f => 
        fs.lstatSync(f).isDirectory() && fs.existsSync(path.join(f, 'icon.png'))
    );
    fs.writeFileSync('icons.json', JSON.stringify(allDirs));
}

run();
