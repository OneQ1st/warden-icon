const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function run() {
    const files = fs.readdirSync('.');
    // 只找根目录下的 png 文件
    const images = files.filter(f => f.endsWith('.png') && fs.lstatSync(f).isFile());

    for (const file of images) {
        const targetDir = file; // 目标目录名：digitalplat.org.png
        const tempFile = `temp_${file}`; // 临时文件名

        try {
            // 1. 先把原图改名，腾出位置
            fs.renameSync(file, tempFile);
            
            // 2. 创建同名文件夹
            if (!fs.existsSync(targetDir)) {
                fs.mkdirSync(targetDir);
            }

            // 3. 处理图片到文件夹内
            await sharp(tempFile)
                .resize(128, 128)
                .toFile(path.join(targetDir, 'icon.png'));
                
            // 4. 删除临时原图
            fs.unlinkSync(tempFile);
            console.log(`✅ 成功将 ${file} 转换为目录结构`);
        } catch (err) {
            console.error(`❌ 处理 ${file} 失败:`, err);
            // 如果失败了，尝试把名字改回来
            if (fs.existsSync(tempFile)) fs.renameSync(tempFile, file);
        }
    }

    // 更新索引
    const allDirs = fs.readdirSync('.').filter(f => 
        fs.lstatSync(f).isDirectory() && 
        f.endsWith('.png') && 
        fs.existsSync(path.join(f, 'icon.png'))
    );
    fs.writeFileSync('icons.json', JSON.stringify(allDirs));
}

run();
