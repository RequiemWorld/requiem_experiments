package {
    import flash.display.Sprite;

    public class SetBackground extends Sprite {
        public function SetBackground() {
            graphics.beginFill(0xFF69B4);
            graphics.drawRect(0, 0, stage.stageWidth, stage.stageHeight);
            graphics.endFill();
        }
    }
}