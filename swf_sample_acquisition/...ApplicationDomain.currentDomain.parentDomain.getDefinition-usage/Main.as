package {
import flash.display.Sprite;
import flash.system.ApplicationDomain;
public class Main extends Sprite {
    public function Main() {
        ApplicationDomain.currentDomain.parentDomain.getDefinition("anything.here.is.Problematic");
    }
}
}