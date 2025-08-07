{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python311Packages.pyTelegramBotAPI
  ];
}
