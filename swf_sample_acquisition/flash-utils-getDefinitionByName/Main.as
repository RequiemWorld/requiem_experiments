package {
	import flash.display.Sprite;
	import flash.utils.getDefinitionByName;
	public class Main extends Sprite {
		public function Main() {
			getDefinitionByName("anything.here.is.Problematic");
		}
	}
}