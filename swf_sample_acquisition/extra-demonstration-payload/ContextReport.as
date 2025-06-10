package {
import flash.display.Stage;
import flash.filesystem.FileStream;
import flash.system.Security;
import flash.system.Capabilities;

public class ContextReport {
    public var securitySandboxType: String;
    public var executedSwfUrl: String;
    public var executedOnOperatingSystemAndPlayer: String;
    public function ContextReport(stage: Stage) {
        securitySandboxType = Security.sandboxType;
        executedSwfUrl = stage.loaderInfo.url;
        executedOnOperatingSystemAndPlayer = Capabilities.os + "/" + Capabilities.playerType;
    }
    public function writeReportToFileStream(fileStream: FileStream): void {
        var reportLinesString: String = "";
        reportLinesString += "securitySandboxType = " + securitySandboxType + "\n"
        reportLinesString += "executedSwfUrl = " + executedSwfUrl + "\n"
        reportLinesString += "executedOnOperatingSystemAndPlayer = " + executedOnOperatingSystemAndPlayer + "\n";
        fileStream.writeMultiByte(reportLinesString, "iso-8859-1");

    }
}
}
