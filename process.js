const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function run() {
    const files = fs.readdirSync('.');
    // 找出根目录下的 png 图片
    const images = files.filter(f => f.toLowerCase().endsWith('.png') && fs.lstatSync(f).isFile());

    for (const file of images) {
        // 【关键修改】：去掉文件名中的 .png 后缀作为文件夹名
        // 例如：digitalplat.org.png -> digitalplat.org
        const targetDir = path.parse(file).name; 
        const tempFile = `temp_${file}`;

        try {
            fs.renameSync(file, tempFile);
            
            if (!fs.existsSync(targetDir)) {
                fs.mkdirSync(targetDir);
            }

            await sharp(tempFile)
                .resize(128, 128)
                .toFile(path.join(targetDir, 'icon.png'));
                
            fs.unlinkSync(tempFile);
            console.log(`✅ 已处理: ${file} -> ${targetDir}/icon.png`);
        } catch (err) {
            console.error(`❌ 处理 ${file} 失败:`, err);
            if (fs.existsSync(tempFile)) fs.renameSync(tempFile, file);
        }
    }

    // 更新索引，只记录不含 .png 后缀的目录
    const allDirs = fs.readdirSync('.').filter(f => {
        return fs.lstatSync(f).isDirectory() && 
               !f.startsWith('.') && 
               f !== 'node_modules' &&
               fs.existsSync(path.join(f, 'icon.png'));
    });
    fs.writeFileSync('icons.json', JSON.stringify(allDirs));
}

run();
