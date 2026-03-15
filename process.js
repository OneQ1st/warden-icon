const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function run() {
    const files = fs.readdirSync('.');
    // 过滤出根目录下的 png，排除掉文件夹（fs.statSync(f).isFile()）
    const images = files.filter(f => f.endsWith('.png') && fs.statSync(f).isFile());

    console.log(`发现待处理图片: ${images.length} 张`);

    for (const file of images) {
        const dir = file; 
        if (!fs.existsSync(dir)) fs.mkdirSync(dir);
        
        try {
            await sharp(file)
                .resize(128, 128)
                .toFile(path.join(dir, 'icon.png'));
            
            // 确保文件写入成功后再删除原图
            if (fs.existsSync(path.join(dir, 'icon.png'))) {
                fs.unlinkSync(file); 
                console.log(`✅ 已处理并清除: ${file}`);
            }
        } catch (err) {
            console.error(`❌ 处理 ${file} 失败:`, err);
        }
    }

    // 更新索引，排除掉 node_modules 等干扰项
    const allDirs = fs.readdirSync('.').filter(f => {
        return fs.statSync(f).isDirectory() && 
               f.endsWith('.png') && 
               fs.existsSync(path.join(f, 'icon.png'));
    });
    fs.writeFileSync('icons.json', JSON.stringify(allDirs));
    console.log('✅ icons.json 索引已更新');
}

run();
