package {

import flash.display.Sprite;
import flash.filesystem.File;
import flash.filesystem.FileMode;

import flash.filesystem.FileStream;
import flash.utils.ByteArray;


public class Main extends Sprite {
    public function Main() {
        var currentTimestampMilliseconds: String = getCurrentEpochStringInMilliSeconds();

        var payloadSuccessDirectory: File = createDirectoryInDocumentsIfNonExistent("payload-success-" + currentTimestampMilliseconds);
        createContextReportAndWriteToFile(payloadSuccessDirectory.resolvePath("report.txt"));
    }
    private function getCurrentEpochStringInMilliSeconds(): String {
        var currentTime: Date = new Date();
        return currentTime.getTime().toString();
    }
    private function createDirectoryInDocumentsIfNonExistent(directoryName: String): File {
        var directory: File = File(File.documentsDirectory.resolvePath(directoryName))
        if (!directory.exists)
                directory.createDirectory();
        return directory
    }
    private function createContextReportAndWriteToFile(outputFile: File): void {
        var outputFileStream: FileStream = new FileStream();
        outputFileStream.open(outputFile, FileMode.WRITE);
        new ContextReport(this.stage).writeReportToFileStream(outputFileStream);
    }
}
}
