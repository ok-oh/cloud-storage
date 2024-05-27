import {ElMessage} from "element-plus";

export default function verifyFileSize(file) {
    if (file) {
        let fileSize = file.size;
        let fileMaxSize = 8 * 1024 * 1024 * 10;
        if (fileSize > fileMaxSize) {
            ElMessage.error("文件不能大于10MB！");
            file.value = "";
            return false;
        } else if (fileSize <= 0) {
            ElMessage.error("文件大小不能为0！");
            file.value = "";
            return false;
        }
        return true
    }
    ElMessage.error("必须传递文件!")
    return false;

}
