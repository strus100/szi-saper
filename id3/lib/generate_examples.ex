defmodule ID3.GenerateExamples do

  @params %{
    beeping: ["yes","no"],
    bomb_visible: ["yes", "no"],
    dugged_up: ["yes","no"],
    grass_color: ["green", "brown", "yellow"],
    is_there_a_big_x_on_this_field: ["yes","no"],
    metal_detector_beeping: ["no","weak","hard"],
    war_here: ["no", "march_of_troops", "trenches"]
  }

  def generate(how_many) do
    how_many =
      1..how_many
      |> Enum.to_list()

    examples = Enum.map(how_many, fn x -> Enum.reduce(@params, [], fn {param_name, param_value}, acc -> acc ++ [Enum.random(param_value)] end) end)

    {:ok, file} = File.open("examples.txt", [:write])
    Enum.each(examples, fn example ->
      Enum.each(example, fn ex -> IO.binwrite(file, "#{ex}, ") end)
      IO.binwrite(file, "\n")
    end)
  end
end

# Enum.map(l, fn x -> Enum.reduce(a,[], fn {k,v},acc -> acc ++ [Enum.random(v)] end) end)
  # a = %{beeping: ["yes","no"], metal_detector_beeping: ["no","weak","hard"], dugged_up: ["yes","no"], war_here: ["no", "march_of_troops", "trenches"], bomb_visible: ["yes", "no"], grass_color: ["green", "brown", "yellow"]}
  # a = %{beeping: ["yes","no"], metal_detector_beeping: ["no","weak","hard"], dugged_up: ["yes","no"], war_here: ["no", "march_of_troops", "trenches"], bomb_visible: ["yes", "no"], grass_color: ["green", "brown", "yellow"], is_there_a_big_x_on_this_field: ["yes","no"]}
