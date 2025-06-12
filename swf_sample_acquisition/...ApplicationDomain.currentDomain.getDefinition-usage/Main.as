package {
	import flash.display.Sprite;
	import flash.system.ApplicationDomain;
	public class Main extends Sprite {
		public function Main() {
			ApplicationDomain.currentDomain.getDefinition("anything.is.problematic.Here");
		}
	}
}