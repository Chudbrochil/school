   M S B A M L   `   `   `  ����  	GalczakP6!    GalczakP6.StoreCheckoutForm   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$A  ;Anthony Galczak - Program 6 - Program Store With a Database��5   	   $	��500��6M   $	��500��6Z   .��5      � ���	#FF8ACD8A.+�5   
   �� $#��C# Office Purchasing Software��6   $
��Left=�68   $��
110,24,0,0q�6S   $	��Top=�6g   $��18(�6   $
��Bold"�6�   �� 5   
   $
��Left=�6   $	��230��60   $��	10,76,0,0q�6=   $	��Top=�6P   $	��300��6h   .@�5      �� -   5         ��Name$ tabFurniture��5      $��	Furniture��6,   .��5	      � ���	#FFE5E5E5$��
0,-1,-6,-1q�6.   $
��Left=�6B   $	��300��6]   .+�5
      �� -   5         ��Name$ lbFurniture��5
      $
��Left=�63   $	��184��6N   $��	10,10,0,0q�6[   $	��Top=�6n   $	��280��6�    �� SelectionMode$ Multiple=�6�   5      5      �� 5      -   5        $ 	tabOffice��5      $��Office Supplies��6)   .��5      � ���	#FFE5E5E5.+�5      �� -   5         ��Name$ cbItem1��5      $��CheckBox��60   $
��Left=�6C   $��	10,10,0,0q�6^   $	��Top=�6q   �� 5      -   5        $ cbItem2��5      $��CheckBox��60   $
��Left=�6C   $��	10,30,0,0q�6^   $	��Top=�6q   �� 5      -   5        $ cbItem3��5      $��CheckBox��60   $
��Left=�6C   $��	10,50,0,0q�6^   $	��Top=�6q   �� 5      -   5        $ cbItem4��5      $��CheckBox��60   $
��Left=�6C   $��	10,70,0,0q�6^   $	��Top=�6q   �� 5      -   5        $ cbItem5��5      $��CheckBox��60   $
��Left=�6C   $��	10,90,0,0q�6^   $	��Top=�6q   5      5      �� 5      -	   5        $ tabComputer��5      $��	Computers��6+   .��5      � ���	#FFE5E5E5.+�5      �� -
   5         ��Name$ btnComputer��5      $��Order a Computer��62   $
��Left=�6M   $��	10,10,0,0q�6h   $	��Top=�6{   $	��274��6�   $��50��6�   $��18(�6�    � ToolTip$1 +Click here to go to the computer order form��6�   �� 5      -   5         ��Name$ txbComputerResults��5      $
��Left=�6:   $	��111��6U   $��	10,81,0,0q�6b    �� TextWrapping$
 Wrap=�6u   $	��Top=�6�   $	��274��6�   "	 �� VerticalScrollBarVisibility$	 Visible=�6�   $,��&Your Computer Order Will Be Shown Here��6�   5      5      5      �� 5   
   -   5        $ 	btnSubmit��5      $��Submit Total Order��6$   $
��Left=�6A   $��315,439,0,0q�6\   $	��Top=�6q   $	��133��6�   6�   �� 5   
   $�� ��6   $
��Left=�6   $��
429,24,0,0q�66   $	��Top=�6J   �� 5   
   -   5        $ 
txbResults��5      $
��Left=�6&   $	��150��6A   $��
10,311,0,0q�6N   $
 Wrap=�6b   $	��Top=�6v   $	��300��6�   $	 Visible=�6�   �� 5    
   -   5        $ 
btnAddFurn��5       $��Add/Update Furniture��6%   $
��Left=�6D   $��315,250,0,0q�6_   $	��Top=�6t   $	��133��6�   6�   �� 5!   
   -   5        $ 
btnDelFurn��5!      $��Delete Furniture��6%   $
��Left=�6@   $��315,275,0,0q�6[   $	��Top=�6p   $	��133��6�   6�   �� 5"   
   $��Furniture Name��6   $
��Left=�6)   $��
315,71,0,0q�6D   $	��Top=�6X   
 J� RenderTransformOrigin$
 0.212,-0.389&�6p   �� 5#   
   -   5        $ txbFurnName��5#      $
��Left=�6'   $��23��6B   $��315,102,0,0q�6N   $
 Wrap=�6c   $	��Top=�6w   $	��167��6�   �� 5$   
   $��Furniture Price��6   $
��Left=�6*   $��315,130,0,0q�6E   $	��Top=�6Z   $	��120��6r   �� 5%   
   -   5        $ txbFurnPrice��5%      $
��Left=�6(   $��23��6C   $��315,161,0,0q�6O   $
 Wrap=�6d   $	��Top=�6x   $	��167��6�   �� 5&   
   $
��Left=�6   $��315,189,0,0q�6/   $
��Wrap=�6D   $O��IIf you are adding or updating Furniture, it must have a name AND a price.��6X   $	��Top=�6�   $��56��6�   $	��167��6�    �� TextAlignment$ Center=�6�   5(      5)      