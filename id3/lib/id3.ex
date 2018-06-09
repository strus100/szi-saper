defmodule ID3 do
  @derive [Poison.Encoder]
  @data_indexes %{beeping: 0, bomb_visible: 1, dugged_up: 2, grass_color: 3, is_there_a_big_x_on_this_field: 4, metal_detector_beeping: 5, war_here: 6, decision: 7}

  def get_data() do
    {:ok, data} = File.read("examples.txt")
    data
    |> String.split("\n")
    |> Enum.map(&(String.split(&1, ", ")))
  end

  def generate_tree(data) do
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
          |> get_factor_with_highest_gain(data, {"", 0})

        IO.puts "Generating for #{factor}"
        IO.inspect data

        tree = Map.put(%{}, "value", factor)

        child_nodes_values = get_factor_values(data, factor)

        Enum.reduce child_nodes_values, tree, fn value, acc ->
          Map.put(acc, value, generate_tree(filter_data(data, factor, value)))
        end
    end
  end

  # Checks whether rest of data map contains only positive or negative examples
  @spec is_yes_or_no(%{}) :: :yes | :no | :look_further
  defp is_yes_or_no(data) do
    cond do
      length(data) == filter_data(data, "decision", "1") |> length -> :yes
      length(data) == filter_data(data, "decision", "0") |> length -> :no
      true -> :look_further
    end
  end

  @spec get_factor_values(%{}, String.t()) :: [String.t()]
  defp get_factor_values(data, factor) do
    factor_index = get_factor_index(factor)
    data
    |> Enum.map(fn x -> Enum.at(x, factor_index) end)
    |> Enum.uniq
  end

  @spec filter_data(%{}, String.t(), number | String.t()) :: %{}
  def filter_data(data, factor, value) do
    index = get_factor_index(factor)
    Enum.filter(data, fn x -> Enum.at(x, index) == value end)
  end

  @spec get_factor_with_highest_gain([String.t()], %{}, {String.t(), number}) :: String.t()
  defp get_factor_with_highest_gain([], _data, {factor, _gain}), do: factor
  defp get_factor_with_highest_gain([head | tail], data, {_factor, gain} = highest_gain) do
    current_gain = gain(data, head)
    if current_gain >= gain do
      get_factor_with_highest_gain(tail, data, {head, current_gain})
    else
      get_factor_with_highest_gain(tail, data, highest_gain)
    end
  end

  @spec gain(%{}, String.t()) :: number
  defp gain(data, factor) do
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

  defp decision_entrophy(data) do
    total_amount = length(data)
    yes_amount = decision_amount(data, "1")
    no_amount = decision_amount(data, "0")

    entrophy(yes_amount, no_amount, total_amount)
  end

  defp decision_amount(list, expected_value) do
    list
    |> Enum.filter(fn x -> List.last(x) == expected_value end)
    |> length
  end

  defp factors_entrophy(data, factor_name, factor_value) do
    total_amount = factor_amount(data, factor_name, factor_value)
    yes_amount = factor_amount(data, factor_name, factor_value, "1")
    no_amount = factor_amount(data, factor_name, factor_value, "0")

    entrophy(yes_amount, no_amount, total_amount)
  end

  defp entrophy(yes, no, total) do
    p_yes = probability(yes, total)
    p_no = probability(no, total)
    (-(p_yes * log2(p_yes)) - (p_no * log2(p_no))) |> Float.round(3)
  end

  defp log2(0.0), do: 0

  defp log2(value) do
    :math.log2(value)
  end

  defp probability(cases, total) do
    cases / total
  end

  defp factor_amount(data, factor_name, expected_value) do
    factor_index = get_factor_index(factor_name)

    data
    |> Enum.filter(fn x -> Enum.at(x, factor_index) == expected_value end)
    |> length
  end

  defp factor_amount(data, factor_name, expected_value, decision) do
    factor_index = get_factor_index(factor_name)

    data
    |> Enum.filter(fn x -> Enum.at(x, factor_index) == expected_value end)
    |> Enum.filter(fn x -> List.last(x) == decision end)
    |> length
  end

  @spec get_factor_index(String.t()) :: Integer
  def get_factor_index(factor_name) do
    factor_name
      |> String.to_atom()
      |> (&Map.get(@data_indexes, &1)).()
  end

  def main() do
    {:ok, file} = File.open "tree.json", [:write]
    json = ID3.generate_tree(ID3.get_data()) |> Poison.encode!()
    IO.binwrite file, json
  end
end
