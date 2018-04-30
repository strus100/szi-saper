#!/usr/local/bin/elixir
defmodule ID3 do
  @derive [Poison.Encoder]
  # is_beeping: yes/no | metal_detector_beeping: no/weak/hard | is_dugged_up: true/false | war_here?: no/march_of_troops/trenches
  @data_indexes %{is_beeping: 0, metal_detector_beeping: 1, is_dugged_up: 2, war_here: 3, decision: 4}
  # @data_indexes %{outlook: 0, temp: 1, humidity: 2, wind: 3, decision: 4}

  # def data do
  #   # outlook / temp / humidity / wind / decision
  #   [
  #     ["Sunny", "Hot", "High", "Weak", 0],
  #     ["Sunny", "Hot", "High", "Strong", 0],
  #     ["Overcast", "Hot", "High", "Weak", 1],
  #     ["Rain", "Mild", "High", "Weak", 1],
  #     ["Rain", "Cool", "Normal", "Weak", 1],
  #     ["Rain", "Cool", "Normal", "Strong", 0],
  #     ["Overcast", "Cool", "Normal", "Strong", 1],
  #     ["Sunny", "Mild", "High", "Weak", 0],
  #     ["Sunny", "Cool", "Normal", "Weak", 1],
  #     ["Rain", "Mild", "Normal", "Weak", 1],
  #     ["Sunny", "Mild", "Normal", "Strong", 1],
  #     ["Overcast", "Mild", "High", "Strong", 1],
  #     ["Overcast", "Hot", "Normal", "Weak", 1],
  #     ["Rain", "Mild", "High", "Strong", 0]
  #   ]
  # end

  def data do
    [
      [1,"hard",1,"trenches",1],
      [1,"weak",1,"march",1],
      [1,"weak",0,"no",1],
      [1,"no",0,"trenches",1],
      [0,"hard",1,"trenches",1],
      [0,"hard",0,"trenches",1],
      [0,"no",1,"no",0],
      [0,"weak",1,"trenches",1],
      [0,"weak",0,"march",0],
      [0,"hard",1,"no",1],
      [0,"weak",1,"no",0]
    ]
  end

  def generate_tree(tree, data) when tree == %{} do
    case is_yes_or_no(data) do
      :yes ->
        "YES"
      :no ->
        "NO"
      _ ->
        factor =
          @data_indexes
          |> Enum.filter(fn {x, _y} -> x != :decision end)
          |> Enum.map(fn {x, _y} -> Atom.to_string(x) end)
          |> get_highest_gain(data, {"", 0})

        tree = Map.put(tree, "value", factor)
        child_nodes_values = get_factor_values(data, factor)
        Enum.reduce child_nodes_values, tree, fn x, acc ->
          Map.put(acc, x, generate_tree(%{}, filter_data(data, factor, x)))
        end
    end
  end

  def is_yes_or_no(data) do
    cond do
      length(data) == filter_data(data, "decision", 1) |> length -> :yes
      length(data) == filter_data(data, "decision", 0) |> length -> :no
      true -> :look_further
    end
  end

  def get_factor_values(data, factor) do
    factor_index = get_factor_index(factor)
    data
    |> Enum.map(fn x -> Enum.at(x, factor_index) end)
    |> Enum.uniq
  end

  def filter_data(data, factor, value) do
    index = get_factor_index(factor)
    Enum.filter(data, fn x -> Enum.at(x, index) == value end)
  end

  def get_highest_gain([], _data, {factor, _gain}), do: factor

  def get_highest_gain([head | tail], data, {_factor, gain} = highest_gain) do
    current_gain = gain(data, head)
    if current_gain > gain do
      get_highest_gain(tail, data, {head, current_gain})
    else
      get_highest_gain(tail, data, highest_gain)
    end
  end

  def gain(data, factor) do
    decision_entrophy = decision_entrophy(data)
    possible_values = get_factor_values(data, factor)

    entrophies =
      for value <- possible_values do
        entrophy = factors_entrophy(data, factor, value)
        probability = factor_amount(data, factor, value) / length(data)
        entrophy * probability
      end

    entrophies
      |> Enum.sum()
      |> Kernel.-(decision_entrophy)
      |> abs
      |> Float.round(3)
  end

  def decision_entrophy(data) do
    total_amount = length(data)
    yes_amount = decision_amount(data, 1)
    no_amount = decision_amount(data, 0)

    entrophy(yes_amount, no_amount, total_amount)
  end

  def decision_amount(list, expected_value) do
    list
    |> Enum.filter(fn x -> List.last(x) == expected_value end)
    |> length
  end

  def factors_entrophy(data, factor_name, factor_value) do
    total_amount = factor_amount(data, factor_name, factor_value)
    yes_amount = factor_amount(data, factor_name, factor_value, 1)
    no_amount = factor_amount(data, factor_name, factor_value, 0)

    entrophy(yes_amount, no_amount, total_amount)
  end

  def entrophy(yes, no, total) do
    p_yes = probability(yes, total)
    p_no = probability(no, total)
    (-(p_yes * log2(p_yes)) - (p_no * log2(p_no))) |> Float.round(3)
  end

  def log2(0.0), do: 0

  def log2(value) do
    :math.log2(value)
  end

  def probability(cases, total) do
    cases / total
  end

  def factor_amount(data, factor_name, expected_value) do
    factor_index = get_factor_index(factor_name)

    data
    |> Enum.filter(fn x -> Enum.at(x, factor_index) == expected_value end)
    |> length
  end

  def factor_amount(data, factor_name, expected_value, decision) do
    factor_index = get_factor_index(factor_name)

    data
    |> Enum.filter(fn x -> Enum.at(x, factor_index) == expected_value end)
    |> Enum.filter(fn x -> List.last(x) == decision end)
    |> length
  end

  def is_factor_clean(data, factor, value) do
    factor_amount(data, factor, value, 0) == 0
  end

  def get_factor_index(factor_name) do
    factor_name
      |> String.to_atom()
      |> (&Map.get(@data_indexes, &1)).()
  end
end
IO.puts "DFVDFVDFV"
{:ok, file} = File.open "tree.json", [:write]
json = ID3.generate_tree(%{}, ID3.data()) |> Poison.encode!()
IO.binwrite file, json

